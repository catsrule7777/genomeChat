import pandas as pd
from langchain.agents import tool

@tool
def merge_vcf(paths):
    """a tool that takes in two comma seperated file paths, and returns the merged result of the two files"""
    paths = paths.split(',')
    vcf_path = paths[0].strip(' ')
    clinvar_path = paths[1].strip(' ')
    vcf = pd.read_csv(vcf_path)
    clinvar = pd.read_csv(clinvar_path)

    vcf['CHROM'] = vcf['CHROM'].str.strip('chr')
    vcf['CHROM'] = vcf['CHROM'].astype(int)
    vcf['POS'] = vcf['POS'].astype(int)
    merged = vcf.merge(clinvar, on=['CHROM', 'POS'], how='inner')

    merged.to_csv('merged.csv')

    return merged