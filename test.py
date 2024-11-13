from typing import Dict, Any
import traceback

''' STANDALONE FUNCTION '''

def eraEscalation(bufugu, platform, l4, l5, l6, l, st, bn):
    era = ""
    bufugu_code = bufugu
    l4_name = l4
    l5_name = l5
    l6_name = l6
    city = l
    province = st
    bufugu_name = bn

    # Platform-based ERA assignments for Personal Banking
    if platform == "Personal Banking":
        if bufugu_code == "G06":
            era = "carla.longauer@rbc.com"
        elif bufugu_code == "G07":
            era = "carla.longauer@rbc.com"
        elif bufugu_code == "G05" and bufugu_name == "Greater Toronto Region Personal Banking":
            era = "inna.talis@rbc.com"
        elif bufugu_code == "G05" and bufugu_name == "Ontario North & East Region Personal Banking":
            era = "linda.ruggiero@rbc.com"
        elif bufugu_code == "G04":
            era = "linda.ruggiero@rbc.com"
        elif bufugu_code == "G01" and bufugu_name == "Atlantic Region Personal Banking":
            era = "darren.clark@rbc.com"
        elif bufugu_code == "G01" and bufugu_name == "British Columbia Region Personal Banking":
            era = "amandeep.gill@rbc.com"
        elif bufugu_code == "G02":
            era = "lynda.cote@rbc.com"
        elif bufugu_code in ["J16", "J13"]:
            era = "breanna.goss@rbc.com"

    # Platform-based ERA assignments for Commercial Banking
    elif platform == "Commercial Banking":
        if bufugu_code in ["G03", "G02", "G06", "G07", "G08", "G05", "G04", "G01", "J18", "J15", "J14", "F54"]:
            era = "neva.lyn.kew@rbc.com"

    # Existing conditions for other BUFUGU codes outside platform-based assignments
    if bufugu_code == "h08":
        if l6_name in ["carter, melissa", "disalle, zanita", "herman, nancy"]:
            era = "theodora.costache@rbc.com"
        else:
            era = "neuza.pento@rbc.com"

    elif bufugu_code == "j15":
        if l4_name in ["howard, roger", "munro, sean"]:
            era = "bethan.dinning@rbc.com"
        else:
            era = "neva.lynkew@rbc.com"

    elif bufugu_code == "h23":
        if l5_name in ["loo, steven", "harrison, pauline"]:
            era = "theodora.costache@rbc.com"
        else:
            era = "marissa.rapagna@rbc.com"

    elif bufugu_code == "g07":
        if l6_name in ["henry, darren"]:
            era = "amandeep.gill@rbc.com"
        else:
            era = "carla.longauer@rbc.com"

    elif bufugu_code == "r21":
        prov_list1 = ["NL", "PE", "NB", "NS"]
        prov_list2 = ["MB", "SK", "AB", "BC"]

        if province in prov_list1:
            era = "eliane.allale@rbc.com"
        elif province in prov_list2:
            era = "eric.drolet@rbc.com"
        elif province == "QC":
            era = "eliane.allale@rbc.com"
        elif province == "ON":
            if city == "toronto":
                era = "eric.drolet@rbc.com"
            else:
                era = "eric.drolet@rbc.com, eliane.allale@rbc.com"
        else:
            era = "eliane.allale@rbc.com"

    elif bufugu_code == "i01":
        if bufugu_name == "advice centres":
            era = "helen.auciello@rbc.com"
        else:
            era = "natalie.vaughan@rbc.com"

    elif bufugu_code == "i03":
        if bufugu_name == "advice centres":
            era = "helen.auciello@rbc.com"
        else:
            era = "natalie.vaughan@rbc.com"

    return era


def assign_era() -> CommandResults:
    era = ""
    bco = "N/A"
    bufugu_code = demisto.getArg("bufugu_code")
    platform = demisto.getArg("platform")  # Retrieve platform argument
    country = demisto.getArg("country")
    city = demisto.getArg("city")
    l4_name = demisto.getArg("l4_name")
    l5_name = demisto.getArg("l5_name")
    l6_name = demisto.getArg("l6_name")
    province = demisto.getArg("province")  # Ensure province is passed correctly
    bufugu_name = demisto.getArg("bufugu_name")
    source_instance = demisto.getArg("source_instance")
    cnb_boolean = demisto.getArg("cnb_boolean")

    # Updated eraEscalationList to include new platform-based codes
    eraEscalationList = ["h08", "h23", "g07", "r21", "i01", "i03", "j17", "g05", "i08", "G06", "G07", "G05", "G04", "G01", "G02", "J16", "J13"]

    if bufugu_code in eraEscalationList:
        era = eraEscalation(bufugu_code, platform, l4_name, l5_name, l6_name, city, province, bufugu_name)
        output = {'Email': era}
    else:
        output = {'Email': ""}

    return CommandResults(
        outputs_prefix='ERA',
        outputs_key_field='',
        outputs=output,
    )


''' MAIN FUNCTION '''
def main():
    try:
        return_results(assign_era())
    except Exception as ex:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute DLPassignERA. Error: {str(ex)}')

''' ENTRY POINT '''
if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
