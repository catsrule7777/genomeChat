import pandas as pd

def merge_vcf(vcf_path, clinvar_path):
    
    vcf = pd.read_csv(vcf_path)
    clinvar = pd.read_csv(clinvar_path)

    vcf['CHROM'] = vcf['CHROM'].str.strip('chr')
    vcf['CHROM'] = vcf['CHROM'].astype(int)
    vcf['POS'] = vcf['POS'].astype(int)
    merged = vcf.merge(clinvar, on=['CHROM', 'POS'], how='inner')

    merged.to_csv('merged.csv')

    return merged
    