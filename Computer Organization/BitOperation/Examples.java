public class Examples {
    int bitVector;
    
    public void clearBitFourOfBitVector() {
        int mask = 0x1;

        mask = mask << 4;

        mask = ~mask;
        
        bitVector = bitVector & mask;
    }

    public void clearBitFourOfBitVectorInOneLine() {
        bitVector = bitVector & ~(0x1 << 4);
    }

    public String rightmostTwoHexDigitsToString(int number)
    {
        String result = "";
        int rightmostHexDigit = number & 0xF;

        if (rightmostHexDigit <= 9) {
            char decimalDigit = (char) ('0' + rightmostHexDigit);
            result = decimalDigit + result;
        }
        else {
            char hexDigit = (char) ('A' + (rightmostHexDigit - 10));
            result = hexDigit + result;
        }

        number = number >> 4;
        rightmostHexDigit = number & 0xF;
        
        if (rightmostHexDigit <= 9) {
            result = (char) ('0' + rightmostHexDigit) + result;
        }
        else {
            result = (char) ('A' + (rightmostHexDigit - 10)) + result;
        }
        return result;
    }
}
