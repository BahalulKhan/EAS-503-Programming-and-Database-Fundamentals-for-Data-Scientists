def determine_data_type(value):
    """
    The function takes a string input and determines its data type to be either a float, int, or string. 
    """
    # BEGIN SOLUTION
    try:
        input_value = float(value)
        if input_value == round(input_value):
            return int
        else:
            return float
    except ValueError:
        return str
    # END SOLUTION


def determine_data_type_of_list(values):
    """
    Write a function whose input is a list of strings. 
    This function determines the correct data type of all the elements in the list. 
    For example, ['1', '2', '3'] is int, ['1.1', '2.2', '3.3'] is float, ['1.1', '2', '3.3'] 
    is also float, and ['1.1', '234String', '3.3'] is str. 
    The purpose of this function to figure out what to cast an array of strings to. 
    Some lists might be all ints, in which case the data type is int. 
    Some might be a mixture of ints and floats, in which case the data type will be a float. 
    Some lists might be a mixture of ints, floats, and strings, 
    in which case the data type of the list will be a string.
    NOTE: This function should use "determine_data_type" function you coded previously

    """
    # BEGIN SOLUTION
    data_types = [determine_data_type(value) for value in values]
    if str in data_types:
        return str
    elif float in data_types:
        return float
    else:
        return int
    # END SOLUTION


def format_sample_fields(format_field, sample_field):
    """
    Write a function whose inputs are a format field and sample field. 
    The format field looks like format_field = 'GT:AD:DP:GQ:PGT:PID:PL' and 
    the sample field looks like

    sample_field = {'XG102': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG103': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG104': '0/1:34,38:72:99:.:.:938,0,796',
                'XG202': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG203': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG204': '0/1:34,38:72:99:.:.:938,0,796',
                'XG302': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG303': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG304': '0/1:34,38:72:99:.:.:938,0,796',
                'XG402': '1/1:0,76:76:99:1|1:48306945_C_G:3353,229,0',
                'XG403': '1/1:0,52:52:99:.:.:1517,156,0',
                'XG404': '0/1:34,38:72:99:.:.:938,0,796'}

    Transform the inputs such that the output looks like this:

    output = {
        'XG102': {'AD': '0,76',
            'DP': '76',
            'GQ': '99',
            'GT': '1/1',
            'PGT': '1|1',
            'PID': '48306945_C_G',
            'PL': '3353,229,0'},
        'XG103': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG104': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'},
        'XG202': {'AD': '0,76',
                'DP': '76',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '1|1',
                'PID': '48306945_C_G',
                'PL': '3353,229,0'},
        'XG203': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG204': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'},
        'XG302': {'AD': '0,76',
                'DP': '76',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '1|1',
                'PID': '48306945_C_G',
                'PL': '3353,229,0'},
        'XG303': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG304': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'},
        'XG402': {'AD': '0,76',
                'DP': '76',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '1|1',
                'PID': '48306945_C_G',
                'PL': '3353,229,0'},
        'XG403': {'AD': '0,52',
                'DP': '52',
                'GQ': '99',
                'GT': '1/1',
                'PGT': '.',
                'PID': '.',
                'PL': '1517,156,0'},
        'XG404': {'AD': '34,38',
                'DP': '72',
                'GQ': '99',
                'GT': '0/1',
                'PGT': '.',
                'PID': '.',
                'PL': '938,0,796'}}
    """

    # BEGIN SOLUTION
    splitted_format_field = format_field.split(":")
    output = {}
    for value, data in sample_field.items():
        splitted_data = data.split(":")
        format_sample = {}
        for i, sample_value in enumerate(splitted_data):
            format_sample[splitted_format_field[i]] = sample_value
        #sorted_format_field = sorted(splitted_format_field)
        #sorted_formatfield_keys = sorted(format_sample.keys(), key=lambda x: sorted_format_field.index(x))
        #sorted_output = {key: format_sample[key] for key in sorted_formatfield_keys}
        output[value] = format_sample
    return output

    # END SOLUTION


def create_dict_from_line(header, line):
    """
    Given the header and a single line, transform them into dictionary as described above. 
    Header and line input are provided in this cell. 

    Write a function whose inputs are a list containing the vcf header and a variant line. 
    The function should return a dictionary using the header as keys and the variant line as values.
     The function should use the format_sample_fields you wrote previously to format the sample fields. 
     The output of the first line looks like this:

    {'ALT': 'G',
    'CHROM': '4',
    'FILTER': 'PASS',
    'ID': '.',
    'INFO': 'AC=1;AF=0.167;AN=6;BaseQRankSum=-2.542;ClippingRankSum=0;DP=180;ExcessHet=3.0103;FS=0;MLEAC=1;MLEAF=0.167;MQ=52.77;MQRankSum=-4.631;QD=0.39;ReadPosRankSum=1.45;SOR=0.758;VQSLOD=-8.209;culprit=MQ;ANNOVAR_DATE=2018-04-16;Func.refGene=intergenic;Gene.refGene=IL2,IL21;GeneDetail.refGene=dist=38536,dist=117597;ExonicFunc.refGene=.;AAChange.refGene=.;Func.ensGene=intergenic;Gene.ensGene=ENSG00000109471,ENSG00000138684;GeneDetail.ensGene=dist=38306,dist=117597;ExonicFunc.ensGene=.;AAChange.ensGene=.;cytoBand=4q27;gwasCatalog=.;tfbsConsSites=.;wgRna=.;targetScanS=.;Gene_symbol=.;OXPHOS_Complex=.;Ensembl_Gene_ID=.;Ensembl_Protein_ID=.;Uniprot_Name=.;Uniprot_ID=.;NCBI_Gene_ID=.;NCBI_Protein_ID=.;Gene_pos=.;AA_pos=.;AA_sub=.;Codon_sub=.;dbSNP_ID=.;PhyloP_46V=.;PhastCons_46V=.;PhyloP_100V=.;PhastCons_100V=.;SiteVar=.;PolyPhen2_prediction=.;PolyPhen2_score=.;SIFT_prediction=.;SIFT_score=.;FatHmm_prediction=.;FatHmm_score=.;PROVEAN_prediction=.;PROVEAN_score=.;MutAss_prediction=.;MutAss_score=.;EFIN_Swiss_Prot_Score=.;EFIN_Swiss_Prot_Prediction=.;EFIN_HumDiv_Score=.;EFIN_HumDiv_Prediction=.;CADD_score=.;CADD_Phred_score=.;CADD_prediction=.;Carol_prediction=.;Carol_score=.;Condel_score=.;Condel_pred=.;COVEC_WMV=.;COVEC_WMV_prediction=.;PolyPhen2_score_transf=.;PolyPhen2_pred_transf=.;SIFT_score_transf=.;SIFT_pred_transf=.;MutAss_score_transf=.;MutAss_pred_transf=.;Perc_coevo_Sites=.;Mean_MI_score=.;COSMIC_ID=.;Tumor_site=.;Examined_samples=.;Mutation_frequency=.;US=.;Status=.;Associated_disease=.;Presence_in_TD=.;Class_predicted=.;Prob_N=.;Prob_P=.;SIFT_score=.;SIFT_converted_rankscore=.;SIFT_pred=.;Polyphen2_HDIV_score=.;Polyphen2_HDIV_rankscore=.;Polyphen2_HDIV_pred=.;Polyphen2_HVAR_score=.;Polyphen2_HVAR_rankscore=.;Polyphen2_HVAR_pred=.;LRT_score=.;LRT_converted_rankscore=.;LRT_pred=.;MutationTaster_score=.;MutationTaster_converted_rankscore=.;MutationTaster_pred=.;MutationAssessor_score=.;MutationAssessor_score_rankscore=.;MutationAssessor_pred=.;FATHMM_score=.;FATHMM_converted_rankscore=.;FATHMM_pred=.;PROVEAN_score=.;PROVEAN_converted_rankscore=.;PROVEAN_pred=.;VEST3_score=.;VEST3_rankscore=.;MetaSVM_score=.;MetaSVM_rankscore=.;MetaSVM_pred=.;MetaLR_score=.;MetaLR_rankscore=.;MetaLR_pred=.;M-CAP_score=.;M-CAP_rankscore=.;M-CAP_pred=.;CADD_raw=.;CADD_raw_rankscore=.;CADD_phred=.;DANN_score=.;DANN_rankscore=.;fathmm-MKL_coding_score=.;fathmm-MKL_coding_rankscore=.;fathmm-MKL_coding_pred=.;Eigen_coding_or_noncoding=.;Eigen-raw=.;Eigen-PC-raw=.;GenoCanyon_score=.;GenoCanyon_score_rankscore=.;integrated_fitCons_score=.;integrated_fitCons_score_rankscore=.;integrated_confidence_value=.;GERP++_RS=.;GERP++_RS_rankscore=.;phyloP100way_vertebrate=.;phyloP100way_vertebrate_rankscore=.;phyloP20way_mammalian=.;phyloP20way_mammalian_rankscore=.;phastCons100way_vertebrate=.;phastCons100way_vertebrate_rankscore=.;phastCons20way_mammalian=.;phastCons20way_mammalian_rankscore=.;SiPhy_29way_logOdds=.;SiPhy_29way_logOdds_rankscore=.;Interpro_domain=.;GTEx_V6_gene=.;GTEx_V6_tissue=.;esp6500siv2_all=.;esp6500siv2_aa=.;esp6500siv2_ea=.;ExAC_ALL=.;ExAC_AFR=.;ExAC_AMR=.;ExAC_EAS=.;ExAC_FIN=.;ExAC_NFE=.;ExAC_OTH=.;ExAC_SAS=.;ExAC_nontcga_ALL=.;ExAC_nontcga_AFR=.;ExAC_nontcga_AMR=.;ExAC_nontcga_EAS=.;ExAC_nontcga_FIN=.;ExAC_nontcga_NFE=.;ExAC_nontcga_OTH=.;ExAC_nontcga_SAS=.;ExAC_nonpsych_ALL=.;ExAC_nonpsych_AFR=.;ExAC_nonpsych_AMR=.;ExAC_nonpsych_EAS=.;ExAC_nonpsych_FIN=.;ExAC_nonpsych_NFE=.;ExAC_nonpsych_OTH=.;ExAC_nonpsych_SAS=.;1000g2015aug_all=.;1000g2015aug_afr=.;1000g2015aug_amr=.;1000g2015aug_eur=.;1000g2015aug_sas=.;CLNALLELEID=.;CLNDN=.;CLNDISDB=.;CLNREVSTAT=.;CLNSIG=.;dbscSNV_ADA_SCORE=.;dbscSNV_RF_SCORE=.;snp138NonFlagged=.;avsnp150=.;CADD13_RawScore=0.015973;CADD13_PHRED=2.741;Eigen=-0.3239;REVEL=.;MCAP=.;Interpro_domain=.;ICGC_Id=.;ICGC_Occurrence=.;gnomAD_genome_ALL=0.0003;gnomAD_genome_AFR=0.0001;gnomAD_genome_AMR=0;gnomAD_genome_ASJ=0;gnomAD_genome_EAS=0.0007;gnomAD_genome_FIN=0.0009;gnomAD_genome_NFE=0.0002;gnomAD_genome_OTH=0.0011;gerp++gt2=.;cosmic70=.;InterVar_automated=.;PVS1=.;PS1=.;PS2=.;PS3=.;PS4=.;PM1=.;PM2=.;PM3=.;PM4=.;PM5=.;PM6=.;PP1=.;PP2=.;PP3=.;PP4=.;PP5=.;BA1=.;BS1=.;BS2=.;BS3=.;BS4=.;BP1=.;BP2=.;BP3=.;BP4=.;BP5=.;BP6=.;BP7=.;Kaviar_AF=.;Kaviar_AC=.;Kaviar_AN=.;ALLELE_END',
    'POS': '123416186',
    'QUAL': '23.25',
    'REF': 'A',
    'SAMPLE': {'XG102': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG103': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG104': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'},
            'XG202': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG203': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG204': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'},
            'XG302': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG303': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG304': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'},
            'XG402': {'AD': '51,8',
                      'DP': '59',
                      'GQ': '32',
                      'GT': '0/1',
                      'PL': '32,0,1388'},
            'XG403': {'AD': '47,0',
                      'DP': '47',
                      'GQ': '99',
                      'GT': '0/0',
                      'PL': '0,114,1353'},
            'XG404': {'AD': '74,0',
                      'DP': '74',
                      'GQ': '51',
                      'GT': '0/0',
                      'PL': '0,51,1827'}}}
    """
    # BEGIN SOLUTION
    line_values = line.strip().split("\t")
    my_dict = {}
    for i in range(0,8):
            my_dict[header[i]] = line_values[i]
    sample_field = {}
    for i in range(9,len(header)):
        sample_field.update({header[i]: line_values[i]})
    for i in range(9,len(header)):
        my_dict['SAMPLE'] = format_sample_fields(line_values[8], sample_field)
    return my_dict
    # END SOLUTION


def read_vcf_file(filename):
    """
    Write a function whose input is a filename for a vcf. 
    The function reads the vcf file one variant at a time and transforms it 
    into a dictionary using the create_dict_from_line function. 
    It returns a list containing all the variant dictionaries. 
    NOTE: Your function should be able to handle multiple lines.
    """
    # BEGIN SOLUTION
    file = open(filename).readlines()
    for header in file:
        if header.startswith("##"):
            continue
        elif header.startswith("#"):
            Header_data = header.strip('#').strip('\n').split('\t')
    data_list = []
    for line in file:
        if line.startswith("##" and "#"):
            continue
        else:
            new_dict = create_dict_from_line(Header_data, line)
            data_list.append(new_dict)
    
    return data_list
    # END SOLUTION


def extract_info_field(data):
    """
    Write a function that extracts the info field from the data dictionary that was 
    created in the previous part. The function should return all the info field dictionaries as list. 
    """
    # BEGIN SOLUTION
    key = 'INFO'
    info_field = [value.get(key) for value in data]
    return info_field
    # END SOLUTION


def create_dictionary_of_info_field_values(data):
    """
    You now need to figure out that data types for each of the info fields. Begin by writing a function that first takes the info fields and turns them into a dictionary. Make sure to skip any fields that do not have a value or are missing a value.

    Note: only return keys that have values! 
    """

    # BEGIN SOLUTION
    output_dict = {}
    for info in data:
        input_dict = dict(info_val.split("=", 1) for info_val in info.split(";") if "=" in info_val)
        for key, value in input_dict.items():
            if value != ".":
                output_dict.setdefault(key, []).append(value)
    Final_dict = {}
    for key, value in output_dict.items():
        Final_values = []
        for info_field_values in value:
            if info_field_values not in Final_values:
                Final_values.append(info_field_values)
        Final_dict[key] = Final_values
    return Final_dict

    # END SOLUTION


def determine_data_type_of_info_fields(data):
    """
    Write a function whose input is the output from create_dictionary_of_info_field_values 
    and uses the previously written function determine_data_type_of_list to determine 
    the data type of each of the info fields. The output is a dictionary whose 
    keys are the name of the info fields and values are the data type. 
    """
    # BEGIN SOLUTION
    output_dict = {}
    for key, values in data.items():
        output_dict[key] = determine_data_type_of_list(values)
    return output_dict
    # END SOLUTION


def format_data(data, info_field_data_type):
    """
    Write a function whose first input is the data from read_vcf_file and 
    the second input is the output from determine_data_type_of_info_fields. 
    The function converts the info field into a dictionary and uses the data types 
    that you determined to cast each field into the correct data type. 
    Make sure to convert the POS to int and QUAL to float. 
    The output will look something like this (I have removed most of the fields):

    The output will look something like this

    {
            "ALT": "G",
            "CHROM": "4",
            "FILTER": "PASS",
            "ID": ".",
            "INFO": {

                "Gene.ensGene": "ENSG00000109471,ENSG00000138684",
                "Gene.refGene": "IL2,IL21",
                "GeneDetail.ensGene": "dist=38306,dist=117597",
                "GeneDetail.refGene": "dist=38536,dist=117597"
            },
            "POS": 123416186,
            "QUAL" :23.25,
            "REF": "A",
            "SAMPLE": {
                "XG102": {
                    "AD": "51,8",
                    "DP": "59",
                    "GQ": "32",
                    "GT": "0/1",
                    "PL": "32,0,1388"
                }
        }

    Additional hints: The function in part 9 takes in two inputs. 
    input #1 is all the data read from lab1_data.vcf and converted into a 
    list of dictionaries where each dictionary corresponds to a line in the vcf file. 
    input #2 is a dictionary that tells you what the data type of each of the info field is.

    The purpose of part 9 is update each of the fields in "data" input so 
    that the data type matches what you have determined it to be previously.
    POS is an integer and QUAL is a float. For the info fields, you have already 
    created a dictionary called info_field_data_type that contains the information 
    for the data type of each of the info field. Now use this to cast the info field 
    into the correct data types.

    And the info field goes from being a string to a nested dictionary.

    NOTE: You can only test this function in the last part! There are not tests for it    

    """
    # BEGIN SOLUTION
    """
    output_lst = []
    for key_variable in data:
        key_variable['POS'] = int(key_variable['POS'])
        key_variable['QUAL'] = float(key_variable['QUAL'])
        info_field_data = key_variable['INFO']
        info_field_values = create_dictionary_of_info_field_values([info_field_data])
        for key, val in info_field_values.items():
            if isinstance(val, list):
                info_field_values[key] = ' '.join(val)
        for key, val in info_field_values.items():
            if key in info_field_data_type:
                info_field_values[key] = info_field_data_type[key](val)
        key_variable['INFO'] = info_field_values
        output_lst.append(key_variable)
    return output_lst
    """
    li3 = []
    for x in data:
        dict2 = {}
        for key,value in x.items():
            if key == 'POS':
                value = int(value)
            elif key == "QUAL":
                value = float(value)
            elif key == 'INFO':
                li = []
                dict1 = {}
                li = value.strip().split(";")
                li2 = []
                for i in li:
                    li2 = i.split("=")
                    if len(li2) > 1 and li2[-1] != ".":
                        d_t = info_field_data_type[li2[0]]
                        dict1[li2[0]] = d_t("=".join(li2[1:]))
                value = dict1
            else:
                value = value
            dict2[key] = value
        li3.append(dict2)
    return li3


            
    # END SOLUTION


def save_data_as_json(data, filename):
    """
    Write a function whose inputs are a Python dictionary and filename. 
    The function will saves the dictionary as a json file using the filename given. 
    Use the json library. 
    Use these options to correctly format your JSON -- 
    sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False. 
    Use this function to save your parsed data as a json file.
    """
    # BEGIN SOLUTION
    import json
    file = open(filename, 'w')
    json.dump(data, file, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)
    file.close()
    # END SOLUTION


def load_data_from_json(filename):
    """
    Write a function whose input is a filename for a json file. 
    The function should use the filename to read the JSON file in 
    which you saved your final parsed data. 
    """
    # BEGIN SOLUTION
    import json
    file = open(filename, 'r')
    data = json.load(file)
    return data
    # END SOLUTION


def find_variant(CHROM, REF, ALT, POS, filename):
    """
    Write a function whose inputs are CHROM, REF, ALT, POS, and filename. 
    Using these inputs, the function should load a JSON file using the given 
    filename and return a list of variants that match the given CHROM, REF, ALT, and POS. 
    """
    # BEGIN SOLUTION
    import json
    file = open(filename, 'r')
    data = json.load(file)
    variants = []
    for info_key in data:
        if all(info_key[key] == value for key, value in {'CHROM': CHROM, 'POS': POS, 'REF': REF, 'ALT': ALT}.items()):
            variants.append(info_key)
    return variants
    # END SOLUTION


def pull_basic_and_predictor_fields(filename):
    """
    Load mini_project1_data.json and pull out all the variants that have a 
    """
    # BEGIN SOLUTION
    output_lst = []
    data = load_data_from_json(filename)
    for key_variable in data:
        predictor_fields = {}
        predictor_value = 0
        for key, value in key_variable['INFO'].items():
            if key in ['FATHMM_pred', 'LRT_pred', 'MetaLR_pred', 'MetaSVM_pred', 'MutationAssessor_pred', 'MutationTaster_pred', 'PROVEAN_pred', 'Polyphen2_HDIV_pred', 'Polyphen2_HVAR_pred', 'SIFT_pred', 'fathmm_MKL_coding_pred']:
                predictor_fields[key] = value
                predictor_value += 0.25 if value == 'L' else 0.5 if value in ['M', 'P'] and key != 'MutationTaster_pred' else 1 if value in ['D', 'A', 'H'] else 0
        predictor_fields['sum_predictor_values'] = predictor_value
        predictor_fields.update({'CHROM': key_variable['CHROM'], 'POS': key_variable['POS'], 'REF': key_variable['REF'], 'ALT': key_variable['ALT']})
        if len(predictor_fields) > 5:
            output_lst.append(predictor_fields)
    return output_lst

    # END SOLUTION

def pull_basic_and_predictor_fields_gzip(filename):
    
    # BEGIN SOLUTION
    import gzip
    with gzip.open(filename, 'rt') as file:
      input_lst = []
      line_value = []
      li_flag = 0
      for line in file:
        if line.startswith('#'):
          header = line.lstrip('#').rstrip().split('\t')
        elif not line.startswith('##'):
          line_value.append(line)
        if li_flag == 1:
            li = []
            li2 = []
            for i in range(0, len(li)):
                li[i].strip().split("\t")
                li2.append(i)           
      for i in range(len(line_value)):
        final = create_dict_from_line(header, line_value[i])
        info_dict = create_dictionary_of_info_field_values(final['INFO'].split())
        final['INFO'] = {}
        if li_flag == 1:
            li = []
            li2 = []
            for i in range(0, len(li)):
                li[i].strip().split("\t")
                li2.append(i)
        for key, val in info_dict.items():
          final['INFO'][key] = ''.join(val)
        input_lst.append(final)
    save_data_as_json(input_lst,"temp.json")
    Final = pull_basic_and_predictor_fields("temp.json")
    save_data_as_json(Final,"mini_project1_gzip.json")
    # END SOLUTION
    

def return_all_non_zero_sum_predictor_values():
    # BEGIN SOLUTION
    load_data = load_data_from_json('mini_project1_gzip.json')
    data = [ele for ele in load_data if ele['sum_predictor_values'] > 0]
    save_data_as_json(data, 'sum_predictor_values_gt_zero.json')
    # END SOLUTION
              

