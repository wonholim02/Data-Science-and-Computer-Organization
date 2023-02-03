public class Bases
{
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

    public static int decimalStringToInt(String decimal) {
        int ans = 0;
        for (int i = 0; i < decimal.length(); i++) {
            ans = 10 * ans + decimal.charAt(i) - '0';
        }
        return ans;
    }

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
