public class Operations
{
    int getShort(int num, int which) {
        return (num >> (which << 4)) & 0xFFFF;
    }
    
    int setByte(int num, int a_byte, int which) {
        return (a_byte << (which << 3)) | (num & (~(0xFF << (which << 3))));
    }
    
    int pack(int s2, int b1, int b0) {
        return (s2 << 16) | ((0xFF & b1) << 8) | (0xFF & b0);
    }

    int bitRange(int num, int s, int n) {
        return (num >> s) & ~(-1 << n);
    }

    int xnor(int num1, int num2) {
        return ~((num1 & ~ num2) | (num2 & ~ num1));
    }

    boolean multipleOf2(int num) {
        return ((num & 1) == 0);
    }

    boolean multipleOf8(int num) {
        return (num & 7) == 0;
    }

    boolean powerOf2(int num) {
        return ((num >= 1) && (((num-1) & num) == 0));
    }
}
