from cyvcf2 import VCF
import pandas as pd
from langchain.agents import tool 

@tool
def clean_vcf(file_path):
    """A tool that takes in a users vcf and then cleans the vcf by extracting useful informatoin and storing it in a csv file - does NOT work with clivnar"""
    data = []
    for variant in VCF(file_path):
        d = {'CHROM' : variant.CHROM, 'POS' : variant.POS, 'ID' : variant.ID, 'REF' : variant.REF, 'ALT' : variant.ALT, 'QUAL' : variant.QUAL, 'FILTER' : variant.FILTER, 'DP' : variant.INFO.get('DP', 0), 'FORMAT' : variant.FORMAT}
        data.append(d)

    df = pd.DataFrame(data)

    df.to_csv(f'{file_path[:len(file_path)-4]}.csv')
    return df

@tool  
def clean_clinvar(file_path):
    """A tool that takes in a clinvar vcf and extracts useful informatoin, and then downloads the new df as a csv"""
    data = []
    
    for variant in VCF(file_path):
        
        d = {'CHROM' : variant.CHROM, 'POS' : variant.POS, 'REF' : variant.REF, 'ALT' : variant.ALT,'CLNSIG' : variant.INFO.get('CLNSIG', 0),
              'CLNHGVS' : variant.INFO.get('CLNHGVS', 0), 'CLNDN' : variant.INFO.get('CLNDN', 0)}
        x = variant.INFO.get('GENEINFO', 0)
        try:
            a, b = x.split(':')
            d['GENEINFO'] = a
        except:
            d['GENEINFO'] = 0
        data.append(d)
    df = pd.DataFrame(data)

    df.to_csv(f'{file_path[:len(file_path)-4]}.csv')
    return df

