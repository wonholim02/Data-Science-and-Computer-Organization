public class Bases
{
    /**
     * Convert a string containing ASCII characters (in binary) to an int.
     *
     * You do not need to handle negative numbers. The Strings we will pass in
     * will be valid binary numbers, and able to fit in a 32-bit signed integer.
     *
     * Example: binaryStringToInt("111"); // => 7
     */
    public static int binaryStringToInt(String binary) {
        int stack = 0;
        int ans = 0;
        int trial = binary.length() - 1;
        while (trial >= 0) {
            if (binary.charAt(trial) == '1') {
                ans += (1 << stack);
            }
            stack = stack + 1;
            trial--;
        }
        return ans;
    }

    /**
     * Convert a string containing ASCII characters (in decimal) to an int.
     *
     * You do not need to handle negative numbers. The Strings we will pass in
     * will be valid decimal numbers, and able to fit in a 32-bit signed integer.
     *
     * Example: decimalStringToInt("46"); // => 46
     *
     * You may use multiplication in this method.
     */
    public static int decimalStringToInt(String decimal) {
        int ans = 0;
        for (int i = 0; i < decimal.length(); i++) {
            ans = 10 * ans + decimal.charAt(i) - '0';
        }
        return ans;
    }

    /**
     * Convert a string containing ASCII characters (in hex) to an int.
     * The input string will only contain numbers and uppercase letters A-F.
     * You do not need to handle negative numbers. The Strings we will pass in will be
     * valid hexadecimal numbers, and able to fit in a 32-bit signed integer.
     *
     * Example: hexStringToInt("A6"); // => 166
     */
    public static int hexStringToInt(String hex) {
        int stack = 0;
        int ans = 0;
        for (int i = 0; i < hex.length(); i++) {
            char character = hex.charAt(hex.length() - i - 1);
            if (character >= 60) {
                ans += ((character - 55) << stack);
            } else {
                ans += ((character - 48) << stack);
            }
            stack += 4;
        }
        return ans;
    }

    /**
     * Convert a int into a String containing ASCII characters (in octal).
     *
     * You do not need to handle negative numbers.
     * The String returned should contain the minimum number of characters
     * necessary to represent the number that was passed in.
     *
     * Example: intToOctalString(166); // => "246"
     *
     * You may declare one String variable in this method.
     */
    public static String intToOctalString(int octal) {
        String ans = "";
        int remainder = 0;
        if (octal == 0) {
            return "0";
        }
        while (octal != 0) {
            int octalNum = 0b111 & octal;
            octal = octal >> 3;
            ans = ((char) (octalNum + 48)) + ans;
        }
        return ans;
    }

    /**
     * Convert a String containing ASCII characters representing a number in
     * binary into a String containing ASCII characters that represent that same
     * value in hex.
     *
     * The output string should only contain numbers and capital letters.
     * You do not need to handle negative numbers.
     * All binary strings passed in will contain exactly 32 characters.
     * The hex string returned should contain exactly 8 characters.
     *
     * Example: binaryStringToHexString("00001111001100101010011001011100"); // => "0F32A65C"
     *
     * You may declare one String variable in this method.
     */
    public static String binaryStringToHexString(String binary) {
        String ans = "";
        int binaryNum  = 0;
        int trial = 31;
        while (trial >= 0) {
            if (binary.charAt(trial) == 49) {
                binaryNum = binaryNum | (1 << (31 - trial));
            }
            trial--;
        }
        int count = 8;
        while (count != 0) {
            int temp = binaryNum & 0xF;
            if (temp + 48 >= 58) {
                ans = ((char) (temp + 55)) + ans;
            } else {
                ans = ((char) (temp + 48)) + ans;
            }
            binaryNum = binaryNum >> 4;
            count--;
        }
        return ans;
    }
}
