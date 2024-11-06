import os.path
import json
import yaml

allPillars = []
allQuestions = {}
tmpAllBestPractice = {}
default_prios = {}

file_path = '../../../waf_model/bestpract_default_priorities.yml'
with open(file_path, 'r') as file:
    default_prios = yaml.safe_load(file)

file_path = '../../../waf_model/qstid-to-code.yml'
with open(file_path, 'r') as file:
    qstid_to_code = yaml.safe_load(file)

file_path = '../../../waf_model/bestpract-to-code.yml'
with open(file_path, 'r') as file:
    answerid_to_bpcode = yaml.safe_load(file)

def awstoolfilename(filename, idx):
    return '../../../data/awstool/'+filename+'-'+str(idx)+'.json'

def convert_to_dict(filename, datakey):

    idx = 0

    data = []
    while os.path.isfile(awstoolfilename(filename, idx)):
        with open(awstoolfilename(filename, idx), 'r') as file:
            data.append( json.load(file) )
        idx += 1

    all = []
    for data_from_datakey in data:
        all = all + data_from_datakey[datakey]

    bigdict = {}
    for item in all:
        allQuestions[item['QuestionId']] = item['PillarId'][:3].upper()
        if(not item['PillarId'] in bigdict):
            bigdict[item['PillarId']] = {}
            if(not item['PillarId'] in allPillars):
                allPillars.append(item['PillarId'])
        bigdict[item['PillarId']][item['QuestionId']] = item
    return bigdict

def list_missing_choices(questionid,selectedch,allch,compact=False):
    missing_dict = {}
    idx=0
    for choice in allch:
        idx=idx+1

        tmpAllBestPractice[choice['ChoiceId']] = qstid_to_code['question_id_to_warcode'][questionid] + "-BP" + str(idx).zfill(2)
        tmpAllBestPractice[qstid_to_code['question_id_to_warcode'][questionid] + "-BP" + str(idx).zfill(2)] = choice['ChoiceId'] + "  TITLE " + choice['Title']

        if not choice['ChoiceId'] in selectedch:
            if(not choice['ChoiceId'][-3:]=='_no'):
                missing_dict[choice['ChoiceId']] = choice
                if( choice['ChoiceId'] in answerid_to_bpcode ):
                    bpcode = answerid_to_bpcode[choice['ChoiceId']]
                    missing_dict[choice['ChoiceId']]['BPCode'] = bpcode

                    if(compact):
                        #default_prios[bpcode]
#                        print(default_prios[bpcode])
                        missing_dict[choice['ChoiceId']]['REPORT'] = {}
                        missing_dict[choice['ChoiceId']]['REPORT']['show'] = default_prios[bpcode]['show']
                        missing_dict[choice['ChoiceId']]['REPORT']['short-med-long'] = default_prios[bpcode]['short-med-long']
                        missing_dict[choice['ChoiceId']]['REPORT']['cost_number_of_100'] = default_prios[bpcode]['cost_number_of_100']
                        missing_dict[choice['ChoiceId']]['REPORT']['importance_number_of_100'] = default_prios[bpcode]['importance_number_of_100']
                        #missing_dict[choice['ChoiceId']]['REPORT'] = default_prios[bpcode]
                        #missing_dict[choice['ChoiceId']]['REPORT'] = bpcode

#                        missing_dict[choice['ChoiceId']]['REPORT']['show'] = False
#                        #missing_dict[choice['ChoiceId']]['REPORT']['suggested-tools-services'] = ''
#                        missing_dict[choice['ChoiceId']]['REPORT']['cost_number_of_100'] = 75
#                        missing_dict[choice['ChoiceId']]['REPORT']['importance_number_of_100'] = 75

#                if(compact):
#                  del missing_dict[choice['ChoiceId']]['Description']

                del missing_dict[choice['ChoiceId']]['ChoiceId']

    return missing_dict
#        else:
#            print("YES " + choice['ChoiceId'])

def create_priority_yaml(compact=False):

    allanswers = convert_to_dict('list-answers', 'AnswerSummaries')
    allimprovement = convert_to_dict('list-lens-review-improvements', 'ImprovementSummaries')

    for pillar in allPillars:

        for key, value in allanswers[pillar].items():
            # TODO
            #if key in allimprovement[pillar]:
            #    allanswers[pillar][key]['ImprovementPlanUrl'] = allimprovement[pillar][key]['ImprovementPlanUrl']
            #else:
            #    allanswers[pillar][key]['ImprovementPlanUrl'] = "MISSING"

            allanswers[pillar][key]['missing_choices'] = list_missing_choices(allanswers[pillar][key]['QuestionId'],allanswers[pillar][key]['SelectedChoices'],allanswers[pillar][key]['Choices'],compact)
            allanswers[pillar][key]['code'] = qstid_to_code['question_id_to_warcode'][allanswers[pillar][key]['QuestionId']]
            del allanswers[pillar][key]['Choices']
            del allanswers[pillar][key]['PillarId']
            del allanswers[pillar][key]['ChoiceAnswerSummaries']
            del allanswers[pillar][key]['Reason']
            del allanswers[pillar][key]['SelectedChoices']
            del allanswers[pillar][key]['IsApplicable']
            del allanswers[pillar][key]['QuestionId']

    return allanswers
