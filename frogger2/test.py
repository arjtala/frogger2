# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

from frogger2.dataset import log_dataset
from frogger2.types import DatasetPrimaryPurpose


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='A simple script to greet a user.')
    parser.add_argument('--gateway', type=str, help='OTel gatewayd.')
    args = parser.parse_args()
    log_dataset(
        dataset_name="CIFAR10",
        description="The CIFAR-10 and CIFAR-100 datasets are labeled subsets of the 80 million tiny images dataset. CIFAR-10 and CIFAR-100 were created by Alex Krizhevsky, Vinod Nair, and Geoffrey Hinton.",
        primary_purpose="test",
        url="https://www.cs.toronto.edu/~kriz/cifar.html",
        oncall="fair_de",
        gateway=args.gateway,
    )
