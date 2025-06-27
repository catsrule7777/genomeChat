from cyvcf2 import VCF
import pandas as pd

print('clean_vcf ran')

def clean_vcf(file_path):
    
    data = []
    for variant in VCF(file_path):
        d = {'CHROM' : variant.CHROM, 'POS' : variant.POS, 'ID' : variant.ID, 'REF' : variant.REF, 'ALT' : variant.ALT, 'QUAL' : variant.QUAL, 'FILTER' : variant.FILTER, 'DP' : variant.INFO.get('DP', 0), 'FORMAT' : variant.FORMAT}
        data.append(d)

    df = pd.DataFrame(data)

    df.to_csv(f'{file_path[:len(file_path)-4]}.csv')
    return df
        
def clean_clinvar(file_path):
    data = []
    for variant in VCF(file_path):
        d = {'CHROM' : variant.CHROM, 'POS' : variant.POS, 'REF' : variant.REF, 'ALT' : variant.ALT,'CLNSIG' : variant.INFO.get('CLNSIG', 0)}
        data.append(d)
    df = pd.DataFrame(data)

    df.to_csv(f'{file_path[:len(file_path)-4]}.csv')
    return df

