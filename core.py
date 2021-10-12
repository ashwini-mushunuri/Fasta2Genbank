import logging
import os
import shutil
from os import getcwd

from Bio import SeqIO
from Bio.SeqFeature import SeqFeature, FeatureLocation
from dnachisel.biotools import genbank_operations

from Emboss import emboss_backtrack


class Core:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)

    def convert_to_nucleotide(self, email, file_path):
        """
        convert protein sequences into nucleotide sequences
        Split multifasta file into multiple files with one sequence each
        :param email:
        :param file_path:
        :return:
        """
        meta = f"{getcwd()}"
        if os.path.exists(f"{meta}\\genbank\\"):
            shutil.rmtree(f"{meta}\\genbank\\")

        if not os.path.exists(f"{meta}\\genbank\\"):
            os.mkdir(f"{meta}\\genbank\\")

        if not os.path.exists(f"{meta}\\temp\\"):
            os.mkdir(f"{meta}\\temp\\")

        out_file = emboss_backtrack(
            email, file_path
        )

        fasta_sequences = SeqIO.parse(open(out_file), "fasta")
        meta = f"{getcwd()}"

        for index, each_fasta_sequence in enumerate(fasta_sequences):
            key = file_path.split('\\')[-1].split('.')[0] + f"-{index}"
            filename = f"temp\\{key}.fasta"
            fasta = ">" + str(each_fasta_sequence.description) + "\n" + str(each_fasta_sequence.seq)
            with open(filename, "w") as f:
                f.write(fasta)
                nucleotide = str(each_fasta_sequence.seq)
                f.close()
                self.convert_to_genbank(nucleotide, each_fasta_sequence, meta, key)

        shutil.make_archive("genbank_files", 'zip', f"{getcwd()}\\genbank")
        return f"{getcwd()}\\genbank_files.zip"

    def convert_to_genbank(self, nucleotide, fasta, meta, key):
        """
        convert each fasta file into genbank file
        Add features
        Add Id to locus
        :param nucleotide:
        :param fasta:
        :param meta:
        :param key:
        :return:
        """
        biopython_record = genbank_operations.sequence_to_biopython_record(
            nucleotide
        )
        biopython_record.description = fasta.description
        biopython_record.features.append(SeqFeature(FeatureLocation(0, len(nucleotide), strand=1), type='CDS'))

        if fasta.id == '<unknown id>':
            id = fasta.description
        else:
            id = fasta.id

        gb_path = f"{meta}\\genbank\\{id}.gb"
        # write genbank file
        genbank_operations.write_record(
            biopython_record, gb_path, file_format="genbank"
        )

        with open(gb_path) as f:
            l = f.readlines()
            # protein_id = re.findall('\[protein_id=.*?\]', "".join(l))[0].split("=")[1].split("]")[0]
            protein_id = id
            l[0] = l[0].replace(".", protein_id)
            with open(gb_path, "w") as f1:
                s = "".join(l)
                f1.writelines(s)
                f1.close()


if __name__ == "__main__":
    core = Core()
    core.convert_to_nucleotide(email='', file_path="fasta_files\\toxin_protein_sample.fasta")
