from os import mkdir, getcwd
from os.path import exists
from shutil import move
from subprocess import check_output


def emboss_backtrack(email, file_name):
    print(f"Converting the fasta file: {file_name}")
    _ = f"{getcwd()}\\temp"
    if not exists(_):
        mkdir(_)
    out_file = "\\".join(["temp", file_name.split("\\")[-1]])
    emboss = getcwd()+"\\"+"webservice-clients-master"
    output = check_output([
        "python",
        f"{emboss}\\emboss_backtranseq.py",
        "--email",
        email,
        "--sequence",
        file_name,
        "--outfile",
        out_file,
        "--outformat",
        "out"
    ])
    out_file = out_file + ".out.txt"
    print(f"Converted file: {out_file} to nucleotide")
    return out_file


def emboss_genbank(email, file_name):
    print(f"Working on file: {file_name}")
    file_name = file_name.strip("\n").strip("\r")
    out_file = "\\".join(file_name.split("\\")[:-2] + ["genbank", file_name.split("\\")[-1]])
    emboss = getcwd()+"\\"+"webservice-clients-master"
    output = check_output([
        "python",
        f"{emboss}\\emboss_seqret.py",
        "--email",
        email,
        "--sequence",
        file_name,
        "--outfile",
        out_file,
        "--stype",
        "dna",
        "--outputformat",
        "out",
        "--outputformat",
        "genbank"
    ])
    out_file = out_file + ".out.txt"
    dest_file = out_file.split(".fasta")[0] + ".gb"
    move(out_file, dest_file)
    _ = out_file.split("\\")[:-2] + ["temp\\"]
    dir = "\\".join(_)
    # rmtree(dir)
    return dest_file
