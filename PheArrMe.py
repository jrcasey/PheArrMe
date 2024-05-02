import src.convert_GBKtoFAA
import src.generateMedia
import src.runCarveBatch
import src.analyzeGapfilling
import src.PheArrPlots
import src.processPheArr

def main():
    src.convert_GBKtoFAA.main()
    src.processPheArr.main()
    src.PheArrPlots.main()
    src.generateMedia.main()
    src.runCarveBatch.main()
    src.analyzeGapfilling.main()

if __name__ == "__main__":
    main()
