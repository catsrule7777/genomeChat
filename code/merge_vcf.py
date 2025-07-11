import pandas as pd
from langchain.agents import tool

@tool
def merge_vcf(paths):
    """a tool that takes in two comma seperated file paths (csv format), and returns the merged result of the two files"""
    paths = paths.split(',')
    vcf_path = paths[0].strip()
    clinvar_path = paths[1].strip()
    vcf = pd.read_csv(vcf_path, dtype=str)
    clinvar = pd.read_csv(clinvar_path, dtype=str)

    vcf['CHROM'] = vcf['CHROM'].str.strip('chr')
    vcf['CHROM'] = vcf['CHROM'].astype(str)
    vcf['POS'] = vcf['POS'].astype(int)

    clinvar['CHROM'] = clinvar['CHROM'].str.strip('chr')
    clinvar['CHROM'] = clinvar['CHROM'].astype(str)
    clinvar['POS'] = clinvar['POS'].astype(int)

    merged = vcf.merge(clinvar, on=['CHROM', 'POS'], how='inner')

    merged.to_csv('merged.csv')

    return merged