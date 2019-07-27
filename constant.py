DB_INPUT_FOLDER = "input"
DB_OUTPUT_FOLDER = "output"
DB_RESULT = DB_OUTPUT_FOLDER + "/" + "DataSetCreator.db"

# ALPHABET = "əƏğĞıIöÖşŞüÜaAbBcCçÇdDeEfFgGhHiİjJkKlLmMnNoOpPqQrRsStTuUvVxXyYzZwW"
ALPHABET = "əğĞıIöşüaAbBcçdDeEfFgGhHiİjJklLmMnNopPqQrRsStTuvVxyYz"

# image pre-processing constants
PADDING = 20
# sizes from initial dataset were averaged around 545
# which means that the average width and height was 545 pixels
# but this size is big for training and will slow down the entire process
# so I decided to use lower size which will also not affect the quality
# since the overall aspect ratio (square) is preserved...
SIZE = 320

PREPROCESSED_OUTPUT_FOLDER = "preprocessed-output"