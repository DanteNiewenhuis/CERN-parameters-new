"""
File consisting of all the benchmarking functions 
"""

from pathlib import Path
import re
import os
import subprocess
from variables import path_to_generated_files, default_variable_values, path_to_iotools, path_to_reference_files, benchmark_datafile_dict


def generate_file(path_to_generator: Path, path_to_reference_file: Path, compression_type: str, cluster_size: int,
                  page_size: int, path_to_output_folder: Path = path_to_generated_files) -> Path:

    file_name = path_to_reference_file.stem
    path_to_output = path_to_output_folder / \
        f"{file_name}~{compression_type}_{page_size}_{cluster_size}.ntuple"

    if path_to_output.exists():
        print(f"output file already available => {path_to_output = }")
        return path_to_output

    os.system(
        f".{path_to_generator.resolve()} -i {path_to_reference_file.resolve()} -o {path_to_output_folder.resolve()} -c {compression_type} -p {page_size} -x {cluster_size}")

    return path_to_output


def run_benchmark(path_to_benchmark: Path, path_to_datafile: Path, cluster_bunch: int, use_rdf: bool) -> str:

    # Get flags
    rdf_flag = "-r" if use_rdf else ""

    # Reset cache
    os.system('sudo sh -c "sync; echo 3 > /proc/sys/vm/drop_caches"')

    # Run benchmark
    out = subprocess.getstatusoutput(
        f"/usr/bin/time  .{path_to_benchmark.resolve()} -i {path_to_datafile.resolve()} -x {cluster_bunch} {rdf_flag} -p")

    return out


def get_runtime(outp: str, target: str = "Runtime-Main:") -> int:
    """Get the runtime of a benchmark based on the output

    Args:
        outp (str): benchmark output
        target (str, optional): what to read out. Defaults to "Runtime-Main:".

    Returns:
        int: the runtime
    """
    for line in outp.split("\n"):
        if target in line:
            return int(line.split(target)[1].strip()[:-2])


def get_metric(outp: str, target: str) -> float:
    """Get a metric from an benchmark output string

    Args:
        outp (str)
        target (str)

    Returns:
        float: value of the given metric
    """
    for line in outp.split("\n"):
        if target in line:

            return float(line.split("|")[-1].strip())


def get_throughput(outp: str) -> float:
    """ Calculate the throughput of a benchmark given its output
        Throughput is defined in MB/s based on the unzipped size, and total processing time

    Args:
        outp (str)

    Returns:
        float
    """
    volume = get_metric(outp, "RNTupleReader.RPageSourceFile.szUnzip")
    volume_MB = volume / 1_000_000

    upzip_time = get_metric(
        outp, "RNTupleReader.RPageSourceFile.timeWallUnzip")
    read_time = get_metric(outp, "RNTupleReader.RPageSourceFile.timeWallRead")
    total_time = upzip_time + read_time

    total_time_s = total_time / 1_000_000_000

    return volume_MB / total_time_s


def get_memory(outp: str) -> float:
    """ Calculate the throughput of a benchmark given its output
        Throughput is defined in MB/s based on the unzipped size, and total processing time

    Args:
        outp (str)

    Returns:
        float
    """
    return int(re.findall(" (\d+)maxresident", outp)[0])


def get_size(path_to_file: Path) -> int:

    return 0


def evaluate_parameters():

    compression_type = default_variable_values["compression_type"]
    cluster_size = default_variable_values["cluster_size"]
    page_size = default_variable_values["page_size"]
    cluster_bunch = default_variable_values["cluster_bunch"]

    benchmark = "lhcb"

    path_to_generator = path_to_iotools / f"gen_{benchmark}"
    path_to_benchmark = path_to_iotools / f"{benchmark}"
    path_to_reference_file = path_to_reference_files / \
        f"{benchmark_datafile_dict[benchmark]}.root"

    print(f"{path_to_generator.exists()}")

    path_to_generated_file = generate_file(path_to_generator, path_to_reference_file,
                                           compression_type, cluster_size, page_size)

    generated_file_size = get_size(path_to_generated_file)

    loops = 10
    for i in loops:
        result_str = run_benchmark(
            path_to_benchmark, path_to_generated_file, cluster_bunch)

        throughput = get_throughput(result_str)
        throughput = get_throughput(result_str)


if __name__ == "__main__":
    print("MAIN")
