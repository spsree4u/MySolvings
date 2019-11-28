# -*- coding: utf-8 -*-
# CB70-6840-3597-44-15-4

import time
import netifaces
import subprocess
import re
import os
import json

from automation.adapters.antivirus.helpers.av_test_utils import ScanUtils
from getmac import get_mac_address
from automation import logger
from automation.constants import DIRECTORIES
import automation.adapters.testing_utilities.helpers.common_test_utils \
    as common_test_utils
from automation.adapters.sep_eg.constants.eg_opstate_constants \
    import FeatureOpState, AssetOpstate
from automation.adapters.install_uninstall.sep_eg.helpers.sep_eg_utils \
    import CommonTestUtils as EGTestUtils
from automation.adapters.antivirus.constants.av_test_constants \
    import TEST_VIRUS_DMG_NAME, UnRepairableVirus, EICARVirus
from automation.adapters.client_sdk.constants.csdk_settings_constants \
    import CSDKFeatureNames
from automation.adapters.antivirus.helpers.av_test_utils \
    import AVTestUtils
from automation.testcases.sep_eg.eg_base_test_script \
    import SEPEGMalwareBaseTestCase, SEPEGAgentFmOpstate, \
    SEPEGOpstateValidationBaseTC
from automation.adapters.sep_eg.constants.eg_events_constants \
    import EventTypes
from automation.frameworks.zen_framework.zen_exceptions \
    import ContinueWithException
from automation.adapters.liveupdate.helpers.lu_settings import LUDatastore
from automation.adapters.client_sdk.csdk_settings_runtime_ips \
    import RuntimeAttributesIPSdefs
from automation.adapters.client_sdk.helpers.csdk_settings_utils \
    import CSDKSettings
from automation.adapters.install_uninstall.sep_eg.helpers.sep_eg_install \
    import Installer
from automation.adapters.user_interface.constants import get_product_version
from automation.core.mac_utilities._account import OSUser
from automation.adapters.all_updatable_tools.lu_tools import LUTool
from automation.adapters.liveupdate.helpers.liveupdate_defs import \
    get_defs_seq
from automation.adapters.liveupdate.constants import \
    LU_TEST_SERVER_OLD_AV_DEFS, LU_TEST_SERVER_OLD_IPS_DEFS
from automation.adapters.liveupdate.helpers.lu_settings import \
    LiveUpdateSettings
from automation.adapters.settings.helpers.settings2_utils import Settings2
from automation.adapters.settings.helpers.settings2_utils import CltmgmtDomain
from automation.adapters.antivirus.constants import DIRECTORIES as av_dirs
from automation.adapters.exceptions.lib_exceptions import RaiseException
from automation.frameworks.zen_framework.zen_utils import Reboot
from automation.adapters.all_updatable_tools.set_language import SetLanguage
from automation.adapters.rabbitmq.establish_connection import \
    TunnelToRabbitMQServer
from automation.constants._directories import TestingDirectory
from automation.constants._autoflex import InputVariables
from automation.frameworks.zen_framework.constants.systeminfo import SystemInfo

TEST_DATA_FOLDER = DIRECTORIES.TESTDATA_FOLDER


######################################################################
# Reference pages for OpState Testing
# https://confluence.ges.symantec.com/display/MTO/Opstate+design
# https://confluence.ges.symantec.com/display/VIX/Health+Status
######################################################################


class TC6664504(SEPEGMalwareBaseTestCase):
    """
        Pre-requisites:
        1. Client is enrolled to the server
        2. Virus definitions are present

        Steps:
        1. Verify unresolved threat details (Fields are below) [v1]
            and verify overall status of product (product_status) [v2]

            hasunresolvedthreats
            unresolvedthreats.first_detected_time
            unresolvedthreats.file.type_id
            unresolvedthreats.file.path
            unresolvedthreats.file.accessor
            unresolvedthreats.file.sha2
            unresolvedthreats.threat.id
            unresolvedthreats.threat.name

        2. Remove unresolved threat files from client machine
        3. Verify unresolved threat details and overall status of
           product (product_status) [v3]

        Expected:
        1. [v1] Threat details should be present in the server
        2. [v2] 'product_status' should be 'COMPROMISED'
        3. [v3] There should not be unresolved threats in Opstate
           and 'product_status' should be 'SECURE'

    """
    Name = 'Malware OpState - Unresolved Threats'
    Description = 'Verify Malware Feature OpState for checking ' \
                  'unresolved threat details and overall status'
    Id = '6664504'

    def __init__(self):
        super().__init__()
        self.virus_class = UnRepairableVirus

    def remove_threats(self):
        # Verify file is deleted or not
        logger.info("Removing threats from the file system...")

        if common_test_utils.remove_file(UnRepairableVirus.virus_file_path) \
                and common_test_utils.unmount_dmg(TEST_VIRUS_DMG_NAME):
            logger.info("Successfully deleted all unresolved threats")
            self.result = self.result or self.SUCCESS
            return self.SUCCESS
        self.result = self.result or self.FAILURE
        raise Exception("Removing unresolved threats failed")

    def server_validation_1(self):
        # Verify event is logged or not
        logger.info("Starting server validations 1...")
        feature_opstate = EGTestUtils.client_device.get_opstate_data()

        if feature_opstate:
            field_names = ["Product Status",
                           "Has Threat Status",
                           "Threat File Type ID",
                           "Threat File Path",
                           "Threat File Accessor",
                           "Threat File SHA2",
                           "Threat ID",
                           "Threat Name"
                           ]
            file_sha2 = common_test_utils.get_sha2_checksum(
                UnRepairableVirus.mounted_path)

            expected_values = [
                FeatureOpState.ProductStatus.COMPROMISED,
                True,
                EventTypes.FileDetection.File.TypeID.FILE,
                UnRepairableVirus.virus_file_path,
                SystemInfo().AUTOFLEX_USERNAME,
                file_sha2,
                UnRepairableVirus.VIRUS_THREAT_ID,
                UnRepairableVirus.VIRUS_THREAT_NAME
            ]
            actual_values = [feature_opstate.get_product_status()]
            product_status_reason = feature_opstate.get_status_reason()

            logger.info("Feature Opstate JSON: \n{}".format(
                feature_opstate.json_data))

            av_opstate = feature_opstate.get_feature_opstate_object(
                feature_name=FeatureOpState.MalwareFeatureOpState.NAME)
            if av_opstate:
                has_threat = av_opstate.get_opstate_hasunresolvedthreats()
                actual_values.append(has_threat)
                logger.info("Verifying Malware Feature OpState fields "
                            "in server log")

                threat_details = av_opstate.get_opstate_unresolved_threat(
                    threat_path=UnRepairableVirus.virus_file_path)
                if threat_details:
                    logger.info("Threat details found")
                    logger.info("Threat First detection time: ".format(
                        threat_details.get_first_detected_time()))
                    threat_data = [threat_details.get_file_type_id(),
                                   threat_details.get_file_path(),
                                   threat_details.get_file_accessor(),
                                   threat_details.get_file_sha2(),
                                   threat_details.get_threat_id(),
                                   threat_details.get_threat_name()]
                    actual_values.extend(threat_data)

                else:
                    logger.error("Retrieving Threat Details failed")
                    actual_values.extend([None] * 6)

                comparison_data = dict(zip(field_names,
                                           zip(actual_values,
                                               expected_values)))
                if actual_values != expected_values:
                    self.result = self.result or self.FAILURE
                    raise ContinueWithException(
                        709,
                        report_message="Mismatch in fields (first value is "
                                       "value from server log) "
                                       "{0}\nStatus Reasons: "
                                       "{1}".format(comparison_data,
                                                    product_status_reason))
                else:
                    logger.info("Unresolved threats are present as expected")
                    logger.info("Fields are matching (first value is value "
                                "from server log) {}".format(comparison_data))
                    self.result = self.result or self.SUCCESS
                    return self.SUCCESS

            else:
                self.result = self.result or self.FAILURE
                raise ContinueWithException(708)

        else:
            self.result = self.result or self.FAILURE
            raise ContinueWithException(7700)

    def server_validation_2(self):
        # Verify event is logged or not
        logger.info("Starting server validations 2...")
        feature_opstate = EGTestUtils.client_device.get_opstate_data()

        if feature_opstate:
            field_names = ["Product Status",
                           "Has Threat Status",
                           "Threat Array"
                           ]

            expected_values = [FeatureOpState.ProductStatus.SECURE,
                               False,
                               []
                               ]
            actual_values = [feature_opstate.get_product_status()]
            product_status_reason = feature_opstate.get_status_reason()

            av_opstate = feature_opstate.get_feature_opstate_object(
                feature_name=FeatureOpState.MalwareFeatureOpState.NAME)
            if av_opstate:
                has_threat = av_opstate.get_opstate_hasunresolvedthreats()
                actual_values.append(has_threat)
                logger.info("Verifying Malware Feature OpState fields "
                            "in server log")

                threat_array = av_opstate.get_opstate_unresolvedthreats()
                if threat_array:
                    logger.error("Threat array is not empty")
                    actual_values.append(threat_array)
                else:
                    actual_values.append([])

                comparison_data = dict(zip(field_names,
                                           zip(actual_values,
                                               expected_values)))
                if actual_values != expected_values:
                    self.result = self.result or self.FAILURE
                    raise ContinueWithException(
                        709,
                        report_message="Mismatch in fields (first value is "
                                       "value from server log) {0}"
                                       "\nStatus Reasons: "
                                       "{1}".format(comparison_data,
                                                    product_status_reason))
                else:
                    logger.info("Unresolved threats are NOT "
                                "present as expected")
                    logger.info("Fields are matching (first value is value "
                                "from server log) {}".format(comparison_data))
                    self.result = self.result or self.SUCCESS
                    return self.SUCCESS
            else:
                self.result = self.result or self.FAILURE
                raise ContinueWithException(708)
        else:
            self.result = self.result or self.FAILURE
            raise ContinueWithException(7700)

    def runTest(self):
        self.result = self.SUCCESS
        self.step("Initial setup for AV testing", self.initial_setup)
        self.step("Generate an unrepairable virus file", self.generate_virus)
        self.step("Verify unresolved threat details and overall status",
                  self.server_validation_1)
        self.step("Remove unresolved threat files from client machine",
                  self.remove_threats)
        self.step("Verify unresolved threat details and overall status "
                  "after removal", self.server_validation_2)


class TC6595839(SEPEGMalwareBaseTestCase):
    """
        Pre-requisites:
        1. Client is enrolled to the server
        2. Virus definitions are present

        Steps:
        1. Check OpState in server [v1]
        2. Disable auto protection
        3. Check OpState in server [v2]
        4. Create/copy a virus file
        5. Verify in machine file created in step 11 is
            deleted or not [v3]
        6. Enable auto protection
        7. Check OpState in server [v4]
        8. Verify in machine file created in step 11 is
            deleted or not [v5]

        Expected:
        1. Feature status and autoprotect status details in OpState
           should be updated in server accordingly

    """
    Name = 'Malware OpState - Enable/Disable'
    Description = 'Verify Malware Feature OpState for checking ' \
                  'Enable/Disable feature and overall status change'
    Id = '6595839'

    virus_obj = EICARVirus()
    virus_obj.VIRUS_FILE_NAME = virus_obj.VIRUS_FILE_NAME + str(Id)

    def server_validation(self, autoprotect_enabled=True):
        # Verify event is logged or not
        logger.info("Starting server validations...")
        feature_opstate = EGTestUtils.client_device.get_opstate_data()

        if feature_opstate:
            field_names = ["Product Status",
                           "Feature State",
                           "Autoprotect State"
                           ]

            if autoprotect_enabled:
                expected_values = [
                    FeatureOpState.ProductStatus.SECURE,
                    FeatureOpState.FeatureStatus.SECURE,
                    FeatureOpState.MalwareFeatureOpState.AutoProtectState.ENABLED
                ]
            else:
                expected_values = [
                    FeatureOpState.ProductStatus.AT_RISK,
                    FeatureOpState.FeatureStatus.AT_RISK,
                    FeatureOpState.MalwareFeatureOpState.AutoProtectState.DISABLED
                ]

            actual_values = [feature_opstate.get_product_status()]
            product_status_reason = feature_opstate.get_status_reason()

            av_opstate = feature_opstate.get_feature_opstate_object(
                feature_name=FeatureOpState.MalwareFeatureOpState.NAME)
            if av_opstate:
                actual_values.extend(
                    [av_opstate.get_feature_status(),
                     av_opstate.get_autoprotect_state()]
                )
                logger.info("Verifying Malware Feature OpState fields "
                            "in server log")

                comparison_data = dict(zip(field_names,
                                           zip(actual_values,
                                               expected_values)))
                if actual_values != expected_values:
                    self.result = self.result or self.FAILURE
                    raise ContinueWithException(
                        709,
                        report_message="Mismatch in fields (first value is "
                                       "value from server log) {0}"
                                       "\nStatus Reasons: "
                                       "{1}".format(comparison_data,
                                                    product_status_reason))
                else:
                    logger.info("Fields are matching (first value is value "
                                "from server log) {}".format(comparison_data))
                    self.result = self.result or self.SUCCESS
                    return self.SUCCESS
            else:
                raise ContinueWithException(708)
        else:
            raise ContinueWithException(7700)

    def check_virus_file_exists(self, path=virus_obj.virus_file_path,
                                file_expected=True, wait_time=5):
        # Verify file is deleted or not
        logger.info("Checking file exists or not...")

        if file_expected:
            if common_test_utils.check_file_deleted(path):
                self.result = self.result or self.FAILURE
                raise ContinueWithException(
                    707,
                    report_message="Virus file {} detected and deleted".format(
                        self.virus_obj.VIRUS_FILE_NAME))
            else:
                logger.info("Virus file {} is not deleted".format(
                    self.virus_obj.VIRUS_FILE_NAME))
                self.result = self.result or self.SUCCESS
                return self.SUCCESS
        else:
            if common_test_utils.check_file_deleted(path, wait_time):
                logger.info("Virus file {} detected and deleted".format(path))
                self.result = self.result or self.SUCCESS
                return self.SUCCESS
            else:
                self.result = self.result or self.FAILURE
                raise ContinueWithException(
                    706,
                    report_message="Virus file {} is not deleted".format(
                        self.virus_obj.VIRUS_FILE_NAME))

    def set_autoprotect(self, unset=False):
        csdk_settings = CSDKSettings()
        ap_feature = csdk_settings.get_feature(
            feature_name=CSDKFeatureNames.AUTO_PROTECT)
        if unset:
            enable = False
            message = "Disabling"
        else:
            enable = True
            message = "Enabling"

        ap_feature.set_feature(enabled=enable, locked=True)
        is_applied = csdk_settings.set_feature(
            feature_name=CSDKFeatureNames.AUTO_PROTECT,
            feature_data=ap_feature.feature)

        if is_applied:
            logger.info(message + " is success")
            self.result = self.result or self.SUCCESS
            return self.SUCCESS
        self.result = self.result or self.FAILURE
        raise ContinueWithException(
            300, "Jira Defect- MACENG-24792(Csdksettings Crash)")

    def runTest(self):
        self.step("Check OpState in server", self.server_validation)
        self.step("Disable auto protection", self.set_autoprotect,
                  unset=True)
        self.step("Check OpState in server", self.server_validation,
                  autoprotect_enabled=False)
        self.step("Create/copy a virus file", AVTestUtils.create_eicar,
                  path=self.virus_obj.virus_file_path)
        self.step("Verify in machine, file created in step 4 "
                  "is deleted or not", self.check_virus_file_exists)
        self.step("Enable auto protection", self.set_autoprotect)
        self.step("Check OpState in server", self.server_validation)

    @property
    def finalResult(self):
        if self.result:
            RaiseException(300, "Etrack/Jira MACENG-24792")
        return self.result


class TC6595958(SEPEGMalwareBaseTestCase):
    """
        Pre-requisites:
        1. Client is enrolled to the server
        2. Virus definitions are present

        Steps:
        1. Validate Malware Feature OpState for last_scan_time and
           last_detection_time [v1]
        2. Perform a scan from the client
        3. Copy virus file to the client machine
        4. Verify in machine, file created in step 4 is deleted or not
        5. Validate Malware Feature OpState for last_scan_time and
           last_detection_time [v2]

        Expected:
        1. last_scan_time and last_detection_time should be updated
           with latest in v2

    """
    Name = 'Malware OpState - Scan and Detection Details'
    Description = 'Verify Malware Feature OpState for checking ' \
                  'last_scan_time and last_detection_time'
    Id = '6595958'

    virus_obj = EICARVirus()
    virus_obj.VIRUS_FILE_NAME = virus_obj.VIRUS_FILE_NAME + str(Id)

    def server_validation(self, scan_start_timestamp=None,
                          detection_start_timestamp=None,
                          initial_validation=False):
        """
        To verify the server for scan time and detection time
        :param scan_start_timestamp: Approximate time when scan started
        :param detection_start_timestamp: Approximate time when virus
        created
        :param initial_validation: if initial_validation is True,
        function will simply log current values of the scan time and
        detection time and skip the part validating the values against
        previous values
        :return: step status
        """
        # Verify event is logged or not
        logger.info("Starting server validations...")

        current_timestamp = int(round(time.time() * 1000))

        feature_opstate = EGTestUtils.client_device.get_opstate_data()

        if feature_opstate:
            av_opstate = feature_opstate.get_feature_opstate_object(
                feature_name=FeatureOpState.MalwareFeatureOpState.NAME)
            if av_opstate:
                logger.info("Verifying Malware Feature OpState fields "
                            "in server log")
                scan_time = av_opstate.get_opstate_last_scan_time()
                detection_time = av_opstate.get_opstate_last_detection_time()

                if initial_validation:
                    logger.info("Getting initial values in server")
                    self.last_scan_timestamp = \
                        int(scan_time) if scan_time else 0
                    self.last_detection_timestamp = \
                        int(detection_time) if scan_time else 0
                    logger.info(
                        "Initial values: last_scan_time={0}, "
                        "last_detection_time={1}".format(
                            scan_time, detection_time))
                    local_result = self.SUCCESS
                    self.result = self.result or local_result

                else:
                    if self.last_scan_timestamp < scan_start_timestamp \
                            < scan_time < current_timestamp:
                        logger.info("Scan time updated with "
                                    "new value {}".format(scan_time))
                        scan_result = self.SUCCESS
                    else:
                        logger.error(
                            "Scan time is NOT updated with correct"
                            " value. Value found is {}".format(scan_time))
                        logger.debug(
                            "Last scan time: {0}\n"
                            "New scan start time: {1}\n"
                            "Logged scan time: {2}\n"
                            "Current time: {3}".format(
                                self.last_scan_timestamp,
                                scan_start_timestamp,
                                scan_time,
                                current_timestamp))
                        scan_result = self.FAILURE

                    if self.last_detection_timestamp \
                            < detection_start_timestamp \
                            < detection_time < current_timestamp:
                        logger.info("Detection time updated with "
                                    "new value {}".format(detection_time))
                        detection_result = self.SUCCESS
                    else:
                        logger.error(
                            "Detection time is NOT updated with "
                            "correct value. Value found is {}".format(
                                detection_time))
                        logger.debug(
                            "Last detection time: {0}\n"
                            "New detection start time: {1}\n"
                            "Logged detection time: {2}\n"
                            "Current time: {3}".format(
                                self.last_scan_timestamp,
                                scan_start_timestamp,
                                scan_time,
                                current_timestamp))
                        detection_result = self.FAILURE

                    local_result = scan_result or detection_result
                    self.result = self.result or local_result

                    # To show the exception in the report,
                    # do a check for self.result
                    if local_result:
                        raise Exception("Wrong Scan/Detection Time. "
                                        "Details (previous time, new time):"
                                        " \nScan time: {0}, {1} \nDetection"
                                        " time: {2}, {3}".format(
                            self.last_scan_timestamp,
                            scan_time,
                            self.last_detection_timestamp,
                            detection_time))

                return local_result
            else:
                raise ContinueWithException(708)
        else:
            raise ContinueWithException(7700)

    def check_virus_file_exists(self, path=virus_obj.virus_file_path):
        # Verify file is deleted or not
        logger.info("Checking file exists or not...")

        if common_test_utils.check_file_deleted(path):
            logger.info("Virus file {} detected and deleted".format(path))
            self.result = self.result or self.SUCCESS
            return self.SUCCESS
        else:
            self.result = self.result or self.FAILURE
            raise ContinueWithException(706)

    def runTest(self):
        self.step("Check OpState in server for last_scan_time and "
                  "last_detection_time", self.server_validation,
                  initial_validation=True)
        detection_start_timestamp = int(round(time.time() * 1000))
        self.step("Create/copy a virus file", AVTestUtils.create_eicar,
                  path=self.virus_obj.virus_file_path)
        scan_start_timestamp = int(round(time.time() * 1000))
        self.step("Perform a file scan from client",
                  ScanUtils().file_scan,
                  path=TEST_DATA_FOLDER)  # check false positive scenario
        self.step("Verify in machine, file created in step 2 "
                  "is deleted or not", self.check_virus_file_exists)
        self.step("Check OpState in server for last_scan_time and "
                  "last_detection_time", self.server_validation,
                  scan_start_timestamp=scan_start_timestamp,
                  detection_start_timestamp=detection_start_timestamp)


class TC6664404(SEPEGOpstateValidationBaseTC):
    """
           Pre-requisites:
           1. Client is enrolled to the server

           Steps:
            1. Validate Machine ID present in the Asset Opstate
            2. Validate Asset Opstate details from client reached server

           Expected:
           v1 - validate the asset details like below should be
           present as part of the Asset Opstate

            1. OS
            2. country
            3. user_name
            4. language
            5. is_virtual
            6. minor_ver
            7. tz_offset
            8. major_ver
            9. computer_name
            11. available_mem
            12. memory_capacity
    """

    Name = 'Asset-Opstate(OS) Details'
    Description = 'Verify Asset-Opstate(OS) Details collected from ' \
                  'Client Vs Json from server '
    Id = '6664404'

    @staticmethod
    def os_detail_in_server(wait=0):

        logger.info("Collecting server_asset_OS information from JSON:\n")
        dict_server = EGTestUtils.client_device.get_device_info(wait_time=wait)
        os_asset_opstate_server = [
            dict_server.get_is_virtual_status(),
            dict_server.get_os_minor_ver(),
            dict_server.get_os_country(),
            dict_server.get_os_ver(),
            dict_server.get_os_tz_offset(),
            dict_server.get_os_major_ver(),
            dict_server.get_os_lang(),
            dict_server.get_os_user(),
            dict_server.get_name(),
            dict_server.get_os_vol_cap_mb(),
            dict_server.get_os_vol_avail_mb()
        ]
        logger.info("os_detail_in_server")
        logger.info(os_asset_opstate_server)
        return os_asset_opstate_server

    @staticmethod
    def os_detail_in_client():

        logger.info("Calling get_os_details library")
        try:
            os_data_client = [
                True,
                common_test_utils.get_os_minor_ver(),
                common_test_utils.get_current_os_locale(),
                common_test_utils.get_os_software_version(),
                common_test_utils.get_timezone_offset(),
                common_test_utils.get_os_major_ver(),
                common_test_utils.get_current_os_language(),
                common_test_utils.get_user_name(),
                SystemInfo.COMPUTERNAME,
                common_test_utils.get_current_volume_capacity_in_mb(),
                common_test_utils.get_current_volume_availability_in_mb()
            ]
            logger.info("os_detail_in_client")
            logger.info(os_data_client)
            return os_data_client
        except Exception as err:
            logger.error(
                " method get_os_details has failed : \n" + str(err))

    def asset_opstate_os_validation(self, wait=0):
        validation_fields = ['is_virtual', 'minor_ver', 'country', 'ver',
                             'tz_offset', 'major_ver', 'lang',
                             'user_name', 'computer_name', 'vol_cap_mb',
                             'vol_avail_mb']
        self.opstate_validation(self.os_detail_in_client(),
                                self.os_detail_in_server(wait=wait),
                                validation_fields, )

    def runTest(self):
        self.step("Validating the Asset-Opstate(OS) Details",
                  self.asset_opstate_os_validation)

    @property
    def finalResult(self):
        if self.result:
            RaiseException(
                300,
                "Jira Defect- MACENG-23344(Asset opstate memory details "
                "incorrect)")
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6725299(SEPEGOpstateValidationBaseTC):
    """
           Pre-requisites:
           1. Client is enrolled to the server

           Steps:
            1. Install the client and get it enrolled
            2. Log on to the Cloud console>devices>click on the
            enrolled devices
                2.1. Validate Asset Opstate (hw) details from
                client reached server

           Expected:
           v1 - validate the asset details like below should be
           present as part of the devices tab in the console

            1. model_vendor
            2. serial
            3. cpu_type
            4. log_cpus
            5. uuid
            6. cpu_mhz
            7.mem_mb
    """

    Name = 'Asset-Opstate(hw) Details'
    Description = 'Verify Asset-Opstate(hw) Details collected from ' \
                  'Client Vs Json from server '
    Id = '6725299'

    @staticmethod
    def get_hw_details_client():
        logger.info("Calling get_os_details library")
        model_data = common_test_utils.get_model_vendor()
        #           in case of physical machine
        #           removing the model version and getting only model vendor name
        if "iMac" in model_data:
            is_virtual = False

        else:
            model_data = re.findall('\d*\D+', model_data)[0]
            is_virtual = True

        hw_data_client = [

            is_virtual,
            model_data,
            common_test_utils.get_cpu_serial_num(),
            common_test_utils.get_cpu_type(),
            common_test_utils.get_num_cores(),
            OSUser.get_hardware_uuid(),
            common_test_utils.get_processor_speed(),
            common_test_utils.get_memory_gb()
        ]
        logger.info(hw_data_client)
        return hw_data_client

    @staticmethod
    def hw_details_in_server(wait=0):
        logger.info("Collecting server_asset_HW information from JSON:\n")
        dict_server = EGTestUtils.client_device.get_device_info(wait_time=wait)
        try:
            model_data = \
                dict_server.get_hw_model_vendor().split(' ')[0].replace(
                    ",", "")
        except Exception as err:
            logger.error("Error in getting model_vendor details, "
                         "maybe a physical machine. Getting model version "
                         "details..." + str(err))
            model_data = dict_server.get_hw_model_version()
        hw_asset_opstate_server = [
            dict_server.get_is_virtual_status(),
            model_data,
            dict_server.get_hw_serial(),
            dict_server.get_hw_cpu_type(),
            dict_server.get_hw_log_cpus(),
            dict_server.get_hw_uuid(),
            dict_server.get_hw_cpu_mhz(),
            int(dict_server.get_hw_mem_mb() / 1000)
        ]

        logger.info(hw_asset_opstate_server)
        return hw_asset_opstate_server

    def hw_details_validation(self, wait=0):
        validation_fields = [
            'is_virtual', 'model_vendor', 'serial', 'cpu_type', 'log_cpus',
            'uuid', 'cpu_mhz', 'mem_mb']
        self.opstate_validation(self.get_hw_details_client(),
                                self.hw_details_in_server(wait=wait),
                                validation_fields)

    def runTest(self):
        self.step(" Validating the Asset-Opstate(HW) Details",
                  self.hw_details_validation)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6756344(SEPEGOpstateValidationBaseTC):
    """
       Pre-requisites:
       1. Client is enrolled to the server

       Steps:
        1. Install SEP-EG in a client machine an dmake sure its
        enrolled to the server.
        2. Check the Asset opstate json after the product install reboot.
        Check for the adapters details in server to be same as in client
        for all the active interfaces.[V1]

       Expected:
       v1 - validate the asset details like below should be
       present as part of the devices tab in the console

        1. Hostname
        2. IPV4
        3. IPv6
        4. Prefix
        5. Mac address
    """

    Name = 'Asset-Opstate(adapters) Details'
    Description = 'Verify Asset-Opstate(adapters) Details collected from ' \
                  'Client Vs Json from server '
    Id = '6756344 '

    @staticmethod
    def adapter_detail_in_server(wait=0):
        logger.info("Collecting server_asset_adapters "
                    "information from JSON:\n")
        dict_server = EGTestUtils.client_device.get_device_info(wait_time=wait)
        mac_addr = get_mac_address()
        interface_details = dict_server.get_adapter_details(mac_addr.upper())
        asset_adapter_server_list = [
            interface_details.get_adapter_host(),
            interface_details.get_adapter_addr(),
            interface_details.get_adapter_ipv4_address(),
            interface_details.get_adapter_ipv6_address(),
            interface_details.get_adapter_ipv6_prefix(),

        ]
        return asset_adapter_server_list

    @staticmethod
    def get_adapter_details_client():
        list_interface = common_test_utils.get_list_of_all_active_interfaces()
        details = []
        for a in list_interface:
            addrs = netifaces.ifaddresses(a)
            link_addr = addrs[netifaces.AF_LINK]
            iface_addrs = addrs[netifaces.AF_INET]
            iface_addrs_6 = addrs[netifaces.AF_INET6]
            iface_dict = iface_addrs[0]
            link_dict = link_addr[0]
            iface6_dict = iface_addrs_6[1]
            hwaddr = link_dict.get('addr')
            iface_addr = iface_dict.get('addr')
            hostname = subprocess.getoutput("hostname")
            ipv6_address = iface6_dict['addr']
            details = [
                hostname,
                hwaddr.upper(),
                iface_addr,
                ipv6_address,
                int(iface6_dict['netmask'].split('/')[1])
            ]
            logger.info(details)
        return details

    def adapter_details_validation(self, wait=0):
        validation_fields = ['host', 'MAC_addr', 'ipv4_addr', 'ipv6_addr',
                             'prefix']
        self.opstate_validation(self.get_adapter_details_client(),
                                self.adapter_detail_in_server(wait=wait),
                                validation_fields)

    def runTest(self):
        self.step(" Validating the Asset-Opstate(adapters) Details",
                  self.adapter_details_validation, wait=320)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6756345(SEPEGOpstateValidationBaseTC):
    """
           Pre-requisites:
           1. Client is enrolled to the server

           Steps:
            1. Install SEP-EG product in client machine and check that
            its enrolled.
            2. Check for the values in the "included_installed_products"
            and validate that these show the expected values. [V1]

           Expected:
           [V1]: Check majorly for the following fields and check if
           the valkues in server and client match:
            1. product_status (expected: SECURE - since the product
            is just installed and AP/IPS are all expected to be in ON position)
            2. version (expected : the product version from SEP-EG->
            about window in client)
            3. agent_status (expected: ONLINE)
            4. name (expected: Symantec Endpoint Protection for Mac)
            5. status_reason (expected as 0)
    """

    Name = 'Asset-Opstate(included_installed_products) Details'
    Description = 'Verify Asset-Opstate(included_installed_products) ' \
                  'Details collected from Client Vs Json from server '
    Id = '6756345'

    @staticmethod
    def get_product_details_client():
        logger.info("Calling get_os_details library")
        try:
            product, version = get_product_version()
            product_data_client = [
                FeatureOpState.ProductStatus.SECURE,
                FeatureOpState.AgentStatus.ONLINE_STATUS,
                AssetOpstate.Status.SECURE,
                version,
                product,

            ]
            logger.info(product_data_client)
            return product_data_client
        except Exception as err:
            logger.error(" method get_os_details has failed : \n" + str(err))

    @staticmethod
    def product_details_in_server(wait=0):
        logger.info("Collecting server_asset_HW information from JSON:\n")
        dict_server = EGTestUtils.client_device.get_device_info(wait_time=wait)
        product_asset_opstate_server = [
            dict_server.get_product_status(),
            dict_server.get_agent_status(),
            dict_server.get_asset_status(),
            dict_server.get_product_version(),
            dict_server.get_product_name()
        ]
        logger.info(product_asset_opstate_server)
        return product_asset_opstate_server

    def product_details_validation(self, wait=0):
        validation_fields = ['product_status', 'agent_status', 'asset_status',
                             'version', 'name']
        self.opstate_validation(self.get_product_details_client(),
                                self.product_details_in_server(wait=wait),
                                validation_fields)

    def runTest(self):
        self.step(" Validating the Asset-Opstate(installed_products) Details",
                  self.product_details_validation)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6748314(SEPEGOpstateValidationBaseTC):
    """
           Pre-requisites:
           1. Client is enrolled to the server

           Steps:
            1. Install the client and get it enrolled
            2. Log on to the Cloud console>devices>click on the
            enrolled devices
                2.1. Validate Asset Opstate details from
                client reached server
            3. Change the os and adapter details like: computer name/ hostname/
             ipv4 addr/ ipv6 addr/language/country [v1]

           Expected:
           v1 - Validate that the os and adapter values are updated in
            asset opstate

            1. Hostname
            2. IPV4
            3. IPv6
            4. Prefix
            5. Mac address
            6. Computer name
            7. Language
            8. Country
        """
    Name = 'Asset-Opstate(adapter) Details after changes in client'
    Description = 'Verify Asset-Opstate(adapter) Details after ' \
                  'changing values in client'
    Id = '6748314'

    def server_validation_modified_values(self, wait=0):
        expected_client_list = TC6756344().get_adapter_details_client()
        expected_client_list.append(common_test_utils.get_computer_name())
        # Force starting the connection to rabbitmq Server since the
        # client ip address is changed and the already established connection
        # to the rabbitmq server is lost.
        if InputVariables().USE_RABBITMQ:
            rabbitmq_data = os.path.join(TestingDirectory.RABBITMQ_DATA,
                                         "rabbitmq_properties.json")
            with open(rabbitmq_data) as fp:
                rabbitmq_properties_dict = json.load(fp)
            test_env = InputVariables().SERVER_ENV
            TunnelToRabbitMQServer().force_start_local_server(
                rabbitmq_properties_dict, test_env)

        actual_server_list = TC6756344().adapter_detail_in_server(wait=wait)
        validation_fields = ['host', 'MAC_addr', 'ipv4_addr', 'ipv6_addr',
                             'prefix', 'computer_name']
        self.opstate_validation(expected_client_list,
                                actual_server_list, validation_fields)

    def runTest(self):
        self.step("Updating Asset OpState Interval",
                  CltmgmtDomain().set_asset_opstate_interval, value=60)
        self.step("Unload SymDaemon", common_test_utils.unload_symdaemon)
        self.step("Load SymDaemon", common_test_utils.load_symdaemon)
        self.step("Getting cltmgmt domain values", Settings2.read, "cltmgmt")
        self.step("Change Computer name",
                  common_test_utils.change_computer_name)
        self.step("Change Hostname",
                  common_test_utils.change_hostname)
        self.step("Change IPv6 address",
                  common_test_utils.change_ipv6_address_ethernet,
                  ipv6_address="fd00::15")
        self.step("Change IPv4 address",
                  common_test_utils.change_ipv4_address_ethernet)
        self.step("Set up DNS for internet to work after ip changes",
                  common_test_utils.set_dns_ip)
        self.step("Validate the modified fields of asset opstate",
                  self.server_validation_modified_values, wait=120)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6778715(SEPEGOpstateValidationBaseTC):
    """
               Pre-requisites:
               1. Client is enrolled to the server
               2. Install the client and get it enrolled
               3. Log on to the Cloud console>devices>click on the
                enrolled devices
                    3.1. Validate Asset Opstate details from
                    client reached server

               Steps:
                1. Change the os details -
                language and country in client machine[v1]

               Expected:
               v1 - Validate that the following os details are
               updated in asset opstate in server as well

                1. Language
                2. Country
            """
    Name = 'Asset-Opstate- change in language and locale'
    Description = 'Verify Asset-Opstate(OS) Details after ' \
                  'changing lang/country in client'
    Id = '6778715'

    def server_validation_modified_values(self, wait=0):
        EGTestUtils.check_enrollment_status_in_server()
        expected_client_list = [
            common_test_utils.get_current_os_locale(),
            common_test_utils.get_current_os_language()
        ]
        dict_server = EGTestUtils.client_device.get_device_info(wait_time=wait)
        actual_server_list = [
            dict_server.get_os_country(),
            dict_server.get_os_lang()]
        validation_fields = ['lang', 'country']
        self.opstate_validation(expected_client_list,
                                actual_server_list, validation_fields)

    def runTest(self):
        self.step("Change Language to French and country name to France",
                  SetLanguage.set_french_language)
        self.step("Rebooting machine for the locale and country changes"
                  " to get reflected in client machine", Reboot().reboot)
        self.step("Validate the modified fields of asset opstate",
                  self.server_validation_modified_values, wait=60)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6664479(SEPEGAgentFmOpstate):
    """
        Pre-requisites:
        1. Install FSD layout of SEP-EG Mac client (but do not reboot).

        Steps:
        1. Before the client machine reboot, capture the json file from the
        server for opstate and validate

        Expected:
        1. Before reboot, reboot source,reason, product status,
        feature status must be updated properly in server.
    """
    Name = 'opstate check- Agent framework- Reboot and product status ' \
           'check during product install'
    Description = "Verify the Agent framework's Pre-reboot contents, must " \
                  "update the reboot reason, reboot source and product status"
    Id = '6664479'

    # Enable developer mode for debugging
    DeveloperMode = True

    def runTest(self):
        self.step("validate agent_framework details before reboot",
                  self.server_validation_general_details)
        self.step("validate server for reboot reason and reboot source values",
                  self.server_validation_reboot_opstate)

    @property
    def finalResult(self):
        # if self.result:
        #     RaiseException(
        #         300,
        #         "Jira Defect- SEP-50929, MACENG-25258"
        #         "(Product status is NOT_COMPUTED)")
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6727493(SEPEGAgentFmOpstate):
    """
        Pre-requisites:
        1. Install FSD layout of SEP-EG Mac client.

        Steps:
        1. Reboot the client machine post product install,
        check for the reboot options in the json file
        from the server for opstates

        Expected:
        1. After reboot, reboot source(empty),reason(empty),
        product status(secure), feature status(secure) must be
        updated properly in server.
    """
    Name = 'opstate check- Agent framework- Reboot and product status ' \
           'check after product install'
    Description = "Verify the Agent framework's Post-reboot contents, must " \
                  "update the reboot reason, reboot source and product status"
    Id = '6727493'

    # Enable developer mode for debugging
    DeveloperMode = True

    def runTest(self):
        self.step("Rebooting the machine post product install",
                  Installer.reboot_post_product_install)
        self.step("Check if virus defs are downloaded",
                  LiveUpdateSettings().verify_virusdefs_existance,
                  wait_time=30)
        self.step("Check if ips defs are downlloaded",
                  LiveUpdateSettings().verify_ipsdefs_existance, wait_time=30)
        self.step("Verify device is enrolled again to fetch device",
                  EGTestUtils.check_enrollment_status_in_server)

        self.step(
            "validate agent_framework details after reboot",
            self.server_validation_general_details,
            feature_status=FeatureOpState.FeatureStatus.SECURE, )
        self.step(
            "validate server that reboot is no longer required "
            "as its already done",
            self.server_validation_reboot_opstate,
            reboot_expected=0)

    @property
    def finalResult(self):
        # if self.result:
        #     RaiseException(
        #         300,
        #         "Jira Defect- SEP-50929, MACENG-25258"
        #         "(Product status is NOT_COMPUTED)")
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6595825(SEPEGOpstateValidationBaseTC):
    """
        Pre-requisites:
        1. Install FSD layout of SEP-EG Mac client and
        have client managed to cloud server.

        Steps:
        1. Check for Basic details of IPS opstate.
        2. Check that network_ips_state and product status in server -[v1]
        3. Disable IPS
        4. Check network_ips_state in server and product status.


        Expected:
        v1. Network_ips_state must be "1" in server and
        product status must be "secure".
        v2. Network_ips_state must be "0" in server and
        product status must be "At Risk".
    """
    Name = 'opstate enable/disable network IPS'
    Description = "Check the IPS opstate details in cloud console"
    Id = '6595825'

    # Enable developer mode for debugging
    DeveloperMode = True

    def __init__(self):
        super().__init__()
        self.result = self.SUCCESS
        self.csdk_obj = CSDKSettings()
        self.feature_obj = self.csdk_obj.get_feature(CSDKFeatureNames.IPS)

    def server_validation_general_details_ips(self):
        """
        @brief: check for general details of ips opstate like sequence
        number/content_download_time/content_type
        @return: None - continue with other tc steps execption
        if the data in client and server do not match
        """
        self.server_validation_1_result = self.SUCCESS
        feature_opstate = EGTestUtils.client_device.get_opstate_data()
        ips_opstate_object = feature_opstate.get_feature_opstate_object(
            feature_name=FeatureOpState.IPSFeatureOpState.NAME)
        expected_agent_fm_details = [
            LUDatastore().get_ips_sequence(),
            LUDatastore().get_ips_version(),
            RuntimeAttributesIPSdefs().get_currentdefsdate(),
            FeatureOpState.FeatureContentType.IPS_content_type,
            FeatureOpState.ProductStatus.SECURE
            if self.feature_obj.get_configuration_enabled()
            else FeatureOpState.ProductStatus.AT_RISK
        ]
        actual_agent_fm_details = [
            ips_opstate_object.get_ips_sequence(),
            ips_opstate_object.get_ips_version(),
            ips_opstate_object.get_ips_content_download_time(),
            ips_opstate_object.get_content_id(),
            feature_opstate.get_product_status()
        ]
        validation_fields = ["sequence", "version",
                             "content_last_download_time", "content_type_id",
                             "product_status"]
        self.opstate_validation(expected_agent_fm_details,
                                actual_agent_fm_details, validation_fields)

    def server_validation_state_check(self, enabled=1):
        """
        @brief: check if ips is disabled/enabled in server and client
        @param enabled: True is IPS is expected to be enabled else False
        @return: None - continue with other tc steps exception
        if the data in client and server do not match
        """
        logger.info("Starting server validation")
        self.server_validation_2_result = self.SUCCESS
        feature_opstate = EGTestUtils.client_device.get_opstate_data()
        ips_object = feature_opstate.get_feature_opstate_object(
            feature_name=FeatureOpState.IPSFeatureOpState.NAME)
        server_ips_state = ips_object.get_network_ips_state()
        client_ips_state = self.feature_obj.get_configuration_enabled()
        expected_product_status = FeatureOpState.ProductStatus.SECURE \
            if enabled else FeatureOpState.ProductStatus.AT_RISK
        logger.info("client state:{0} \n server ips state:{1} \n "
                    "expected_status:{2}".format(str(client_ips_state),
                                                 server_ips_state,
                                                 expected_product_status))
        if client_ips_state == enabled == server_ips_state:
            logger.info("IPS state same in server and client")
            if feature_opstate.get_product_status() == expected_product_status:
                logger.info("product status has changed based on IPS setting")
                self.server_validation_2_result = self.SUCCESS
        else:
            logger.error("IPS state different in server and client")
            self.server_validation_2_result = self.FAILURE
        self.result = self.result or self.server_validation_2_result
        if self.server_validation_2_result:
            raise ContinueWithException(
                300,
                "Jira Defect- MACENG-24580(Wrong Network ips state opstate "
                "when ips turned off)", "Mismatch in ips state of client {0} "
                                        "and server {1}".format(
                    str(client_ips_state),
                    str(server_ips_state)))
        return self.server_validation_2_result

    def enable_disable_ips(self, enabled=1):
        """
        @brief: Enable/disable IPS
        @param enabled: True if IPS must be enabled else False
        @return: None - continue with other tc steps exception
        if the data in client and server do not match
        """

        set_ips = self.feature_obj.set_ips_state(enabled=enabled, locked=True)
        result = self.csdk_obj.set_feature(feature_name=CSDKFeatureNames.IPS,
                                           feature_data=set_ips)
        if not result:
            RaiseException(
                300, "Jira Defect- MACENG-24792(Csdksettings Crash)")

    def runTest(self):
        self.step(
            "Validate the IPS basic details available "
            "in cloud console",
            self.server_validation_general_details_ips)
        self.step(
            "validate IPS is enabled in server",
            self.server_validation_state_check,
            enabled=FeatureOpState.IPSFeatureOpState.NetworkIPSState.ENABLED)
        self.step("Disable IPS in client", self.enable_disable_ips,
                  enabled=FeatureOpState.
                  IPSFeatureOpState.NetworkIPSState.DISABLED)
        self.step(
            "Validate IPS is disabled in server",
            self.server_validation_state_check,
            enabled=FeatureOpState.IPSFeatureOpState.NetworkIPSState.DISABLED)
        self.step(
            "Validate the IPS basic details available "
            "in cloud console after IPS is disabled",
            self.server_validation_general_details_ips)
        self.step("Enable IPS in client",
                  self.enable_disable_ips,
                  enabled=FeatureOpState.
                  IPSFeatureOpState.NetworkIPSState.ENABLED)
        self.step(
            "Validate IPS is enabled in server",
            self.server_validation_state_check,
            enabled=FeatureOpState.IPSFeatureOpState.NetworkIPSState.ENABLED,
            return_value=self.SUCCESS)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6758715(SEPEGOpstateValidationBaseTC):
    """
        Pre-requisites:
        1. The SEP_EG product must be installed in Mac client and enrolled
        with Server, the latest protection defs must be available
        2. The product and IPS feature status must be "SECURE"
        3. Old protection defs must be uploaded/available in a test server

        Steps:
        1. Run the DeleteIPSSignatures.command from the "Allupdatable tools"
        and make sure the vulnprotectiondefs are removed from the path-[v1][v2]
        2. Point the LU server to a local server where old protection defs are
        housed using SetHostForLUX.command from "Allupdatabel tools" folder,
        3. Run the LU and check that old protection defs(older by atleast
        30days) are downloaded after successful LU run.---[v3]
        4. Check for the IPS feature and product status. [v4]
        5. Run the PointToPublicServers.command in "Allupdatable tools" folder
        and run LU --[v5]

        Expected:
        [v1] Check that the sequence number for IPS opstate in postman shows 0
        as the defs are deleted.
        [v2] The feature status and product status is at "AT_RISK" as the
        network_ips_state is set to 4 in ips feature opstate
        [V3] Check that the sequence number for IPS opstate in postman shows
        old date as the defs are outdated.
        [v4] The feature and product status must be "AT_RISK"
        [v5] check that the latest protection defs are downloaded in client
         and IPS feature and product status are at "SECURE"
    """
    Name = 'IPS Feature status and product status change when ' \
           'protectiondefs are outdated(by atleast 30days)'
    Description = "Verify that when protection defs are outdated, the IPS " \
                  "feature status and product stauts change to 'AT_RISK'"
    Id = '6758715'

    # Enable developer mode for debugging
    DeveloperMode = True

    def ips_defs_opstate_validation(self, feature_state, product_state,
                                    network_ips_state,
                                    status_reason, wait=30):
        logger.info("Starting server validation for ips")
        self.server_validation_result = self.SUCCESS
        feature_opstate = EGTestUtils.client_device.get_opstate_data(
            wait_time=wait)
        ips_object = feature_opstate.get_feature_opstate_object(
            feature_name=FeatureOpState.IPSFeatureOpState.NAME)
        expected_client_details = \
            [
                network_ips_state,
                get_defs_seq(),
                feature_state,
                product_state,
                status_reason
            ]
        actual_server_details = \
            [
                ips_object.get_network_ips_state(),
                ips_object.get_ips_sequence(),
                ips_object.get_feature_status(),
                feature_opstate.get_product_status(),
                ips_object.get_status_reason()
            ]

        validation_fields = ["network_ips_state", "seq_num", "feature_state",
                             "product_state", "status_reason"]
        logger.info("Content last download time is "
                    "{0}".format(ips_object.get_ips_content_download_time()))
        self.opstate_validation(expected_client_details, actual_server_details,
                                validation_fields)

    def runTest(self):
        self.step("Verify device is enrolled again to fetch device",
                  EGTestUtils.check_enrollment_status_in_server)
        self.step("Verify IPS defs are available in client",
                  LiveUpdateSettings().verify_ipsdefs_existance,
                  return_value=1)

        self.step(
            "Verify the fields in IPS opstate",
            self.ips_defs_opstate_validation,
            feature_state=FeatureOpState.FeatureStatus.SECURE,
            product_state=FeatureOpState.ProductStatus.SECURE,
            network_ips_state=FeatureOpState.IPSFeatureOpState.NetworkIPSState.ENABLED,
            status_reason=[
                FeatureOpState.IPSFeatureOpState.StatusReason.IPS_NETWORK_STATE_IS_1])
        self.step("Delete the protection defs from client",
                  LiveUpdateSettings.remove_ips_defs)
        self.step("Verify IPS defs are deleted",
                  LiveUpdateSettings().verify_ipsdefs_existance,
                  return_value=0)
        self.step("Point the LU server to a test server with old defs"
                  "(older by atleat 30 days)", LUTool.point_lu_to_host,
                  LU_TEST_SERVER_OLD_IPS_DEFS)
        self.step("Run LU tool", LiveUpdateSettings.run_lu)
        self.step("Rebooting the client machine as old defs require a restart",
                  Reboot().reboot)
        self.step("Creating client after reboot",
                  EGTestUtils.check_enrollment_status_in_server)
        self.step(
            "Verify the fields in IPS opstate",
            self.ips_defs_opstate_validation,
            feature_state=FeatureOpState.FeatureStatus.AT_RISK,
            product_state=FeatureOpState.ProductStatus.AT_RISK,
            network_ips_state=FeatureOpState.IPSFeatureOpState.NetworkIPSState.ENABLED,
            status_reason=[
                FeatureOpState.IPSFeatureOpState.StatusReason.IPS_NETWORK_STATE_IS_1,
                FeatureOpState.IPSFeatureOpState.StatusReason.IPS_CONTENT_TYPE_ID_OR_SEQ_MISMATCH],
            wait=100)
        self.step("Delete the protection defs from client",
                  LiveUpdateSettings.remove_ips_defs)
        self.step("Point the LU server to the production server to get "
                  "latest protection defs", LUTool.point_lu_to_public_server)
        self.step("Run LU tool", LiveUpdateSettings.run_lu)
        self.step(
            "Verify the fields in IPS opstate",
            self.ips_defs_opstate_validation,
            feature_state=FeatureOpState.FeatureStatus.SECURE,
            product_state=FeatureOpState.ProductStatus.SECURE,
            network_ips_state=FeatureOpState.IPSFeatureOpState.NetworkIPSState.ENABLED,
            status_reason=[
                FeatureOpState.IPSFeatureOpState.StatusReason.IPS_NETWORK_STATE_IS_1],
            wait=60)

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass


class TC6758714(SEPEGOpstateValidationBaseTC):
    """
        Pre-requisites:
        1. The SEP_EG product must be installed in Mac client and enrolled with
         Server, the latest virus defs must be available in the client
        2. The product and feature status must be "SECURE"
        3. Old virus defs must be uploaded/available in a test server

        Steps:
        1. Run the DeleteVirusDefinitions.command from the "Allupdatable tools"
         and make sure the virusdefs are removed ---[v1][v2]
        2. Point the LU server to a local server where old defs are housed
        using SetHostForLUX.command from "Allupdatabel tools" folder
        3. Run the LU and check that old virus defs(older by atleast 30days)
        are downloaded after successful LU run.---[v3]
        4. Check for the feature and product status. [v4]
        5. Run the PointToPublicServers.command in "Allupdatable tools"
        folder and run LU --[v5]

        Expected:
        [V1] Check that the sequence number for Malware opstate in postman
        shows 0 as the defs are deleted.
        [v2] The Malware feature status and product status is at "SECURE"
        [V3] Check that the sequence number for Malware opstate in postman
        shows old date as the defs are outdated.
        [v4] The feature and product status must be "AT_RISK"
        [v5] The new virus definitions must get downloaded after
        successfull LU in client.
        The Malware feature and product status must show "SECURE".
    """
    Name = 'Malware Feature status and product status change when ' \
           'virusdefs are outdated(by atleast 30days)'
    Description = "Verify that when protections defs are outdated, the " \
                  "Malware feature status and product stauts change to AT_RISK"
    Id = '6758714'

    # Enable developer mode for debugging
    DeveloperMode = True

    def malware_defs_opstate_validation(self, feature_state, product_state,
                                        status_reason, wait=30):
        logger.info("Starting server validation for malware")
        self.server_validation_result = self.SUCCESS
        feature_opstate = EGTestUtils.client_device.get_opstate_data(
            wait_time=wait)
        malware_object = feature_opstate.get_feature_opstate_object(
            feature_name=FeatureOpState.MalwareFeatureOpState.NAME)
        expected_client_details = \
            [
                get_defs_seq(
                    defs_location=av_dirs.SILO_VIRUS_DEFS),
                feature_state,
                product_state,
                status_reason
            ]

        actual_server_details = \
            [
                malware_object.get_malware_sequence(),
                malware_object.get_feature_status(),
                feature_opstate.get_product_status(),
                malware_object.get_status_reason()
            ]

        validation_fields = ["seq_num", "feature_state",
                             "product_state", "status_reason"]
        logger.info("Content last download time is {0}".format(
            malware_object.get_opstate_content_last_download_time())
        )
        self.opstate_validation(expected_client_details,
                                actual_server_details, validation_fields)

    def runTest(self):
        self.step("Verify device is enrolled again to fetch device",
                  EGTestUtils.check_enrollment_status_in_server)
        self.step("Verify defs are available in client",
                  LiveUpdateSettings().verify_virusdefs_existance,
                  return_value=1)

        self.step(
            "Verify the fields in Malware opstate",
            self.malware_defs_opstate_validation,
            feature_state=FeatureOpState.FeatureStatus.SECURE,
            product_state=FeatureOpState.ProductStatus.SECURE,
            status_reason=[
                FeatureOpState.MalwareFeatureOpState.StatusReason.MALWARE_PROTECTION_AUTO_PROTECT_IS_1])
        self.step("Delete the malware defs from client",
                  LiveUpdateSettings.remove_virus_defs)
        self.step("Verify virus defs are deleted",
                  LiveUpdateSettings().verify_virusdefs_existance,
                  return_value=0)
        self.step("Point the LU server to a test server with old defs"
                  "(older by atleat 30 days)", LUTool.point_lu_to_host,
                  LU_TEST_SERVER_OLD_AV_DEFS)
        self.step("Run LU tool", LiveUpdateSettings.run_lu)
        self.step("check old defs are available",
                  LiveUpdateSettings().verify_virusdefs_existance,
                  return_value=0)
        self.step(
            "Verify the fields in Malware opstate",
            self.malware_defs_opstate_validation,
            feature_state=FeatureOpState.FeatureStatus.AT_RISK,
            product_state=FeatureOpState.ProductStatus.AT_RISK,
            status_reason=[
                FeatureOpState.MalwareFeatureOpState.StatusReason.MALWARE_PROTECTION_AUTO_PROTECT_IS_1,
                FeatureOpState.MalwareFeatureOpState.StatusReason.MALWARE_PROTECTION_CONTENT_TYPE_ID_OR_SEQ_MISMATCH])
        self.step("Delete the malware defs from client",
                  LiveUpdateSettings.remove_virus_defs)
        self.step("Point the LU server to the production server to get "
                  "latest protection defs", LUTool.point_lu_to_public_server)
        self.step("Run LU tool", LiveUpdateSettings.run_lu)
        self.step("Verify new defs are downloaded",
                  LiveUpdateSettings().verify_virusdefs_existance,
                  return_value=1)
        self.step(
            "Verify the fields in Malware opstate",
            self.malware_defs_opstate_validation,
            feature_state=FeatureOpState.FeatureStatus.SECURE,
            product_state=FeatureOpState.ProductStatus.SECURE,
            status_reason=[
                FeatureOpState.MalwareFeatureOpState.StatusReason.MALWARE_PROTECTION_AUTO_PROTECT_IS_1])

    @property
    def finalResult(self):
        return self.result

    @classmethod
    def tearDown(cls):
        pass
