"""
This module contains the main function of "Bus Tracker".
"""

from datetime import datetime
from BTlibs.EDA import EDA
from BTlibs.preprocessing import preprocessing
from BTlibs.modules import conv_lstm


def main():
    """
    demo function.
    """
    eda = EDA.EDAPerformer()
    preprocess = preprocessing.Preprocess()
    module = conv_lstm.ConvLSTMInputBuilder()

    eda.start()
    preprocess.start()
    module.start()
    return 0


if __name__ == "__main__":
    start = datetime.now()
    main()
    print(f"Bus tracker done. Duration: {datetime.now() - start}")
