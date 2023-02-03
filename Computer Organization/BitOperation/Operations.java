public class Operations
{
    /**
     * Get an 16-bit short from an int.
     *
     * Ints are made of 2 shorts, numbered like so:
     *   |       B1       |      B0        |
     *
     * For a graphical representation of the bits:
     *
     * bit 31                           bit 0
     *    v                               v
     *    1101100000001100 0001111111011001
     *   +----------------+----------------+
     *   |       B1       |       B0       |
     *
     * Examples:
     *     getShort(0x56781234, 0); // => 0x1234
     *     getShort(0x56781234, 1); // => 0x5678
     *
     * Note: Remember, no multiplication allowed!
     *
     * @param num The int to get a short from.
     * @param which Determines which short gets returned - 0 for
     *              least-significant short.
     *
     * @return A short corresponding to the "which" parameter from num.
     */
    int getShort(int num, int which) {
        return (num >> (which << 4)) & 0xFFFF;
    }

    /**
     * Set a specified 8-bit byte in an int with a provided 8-bit value.
     *
     * Ints are made of 4 bytes, numbered like so:
     *   |   B4   |   B2   |   B1   |   B0   |
     *
     * For a graphical representation of the bits:
     *
     * bit 31                             bit 0
     *    v                                 v
     *    11011000 00001100 00011111 11011001
     *   +--------+--------+--------+--------+
     *   |   B3   |   B2   |   B1   |   B0   |
     *
     * Examples:
     *     setByte(0xAAA5BBC6, 0x25, 0); // =>  0xAAA5BB25
     *     setByte(0x56B218F9, 0x80, 3); // =>  0x80B218F9
     *
     * Note: Remember, no multiplication allowed!
     *
     * @param num The int that will be modified.
     * @param a_byte The byte to insert into the integer.
     * @param which Selects which byte to modify - 0 for least-significant
     * byte.
     *
     * @return The modified int.
     */
    int setByte(int num, int a_byte, int which) {
        return (a_byte << (which << 3)) | (num & (~(0xFF << (which << 3))));
    }

    /**
     * Pack a short and 2 bytes into an int.
     *
     * The short and 2 bytes should be placed consecutively in the 32-bit int in
     * the order that they appear in the parameters
     *
     * Example:
     *     pack(0x1234, 0x56, 0x78); // => 0x12345678
     *     pack(0xCOFF, 0xEE, 0x10); // => 0xCOFFEE10
     *
     * @param s2 Most significant short (will always be a 16-bit number).
     * @param b1 2nd least significant byte (will always be a 8-bit number).
     * @param b0 Least Significant byte (will always be a 8-bit number).
     *
     * @return a 32-bit value formatted like so: s2b1b0
     */
    int pack(int s2, int b1, int b0) {
        return (s2 << 16) | ((0xFF & b1) << 8) | (0xFF & b0);
    }

    /**
     * Extract a range of bits from a number.
     *
     * Examples:
     *     bitRange(0x00001234, 0, 4);  // => 0x00000004
     *     bitRange(0x00001234, 4, 8);  // => 0x00000023
     *     bitRange(0x12345678, 0, 28); // => 0x02345678
     *     bitRange(0x55555555, 5, 7);  // => 0x0000002A
     *
     * Note: We will only pass in values 1 to 32 for n.
     *
     * @param num An n-bit 2's complement number.
     * @param s The starting bit to grab
     * @param n The number of bits to return.
     * @return The n-bit number num[s:s+n-1].
     */
    int bitRange(int num, int s, int n) {
        return (num >> s) & ~(-1 << n);
    }

    /**
     * NOTE: For this method, you may only use &, |, and ~.
     *
     * Perform an exclusive-nor on two 32-bit ints. That is, take their
     * exclusive-or and bitwise-not the result.
     *
     * Examples:
     *     xnor(0xFF00FF00, 0x00FF00FF); // => 0x00000000
     *     xnor(0x12345678, 0x87654321); // => 0x6AAEEAA6
     *
     * @param num1 An int
     * @param num2 Another int
     *
     * @return num1 XNOR num2
     */
    int xnor(int num1, int num2) {
        return ~((num1 & ~ num2) | (num2 & ~ num1));
    }

    /**
     * Return true if the given number is a multiple of 2.
     *
     * Examples:
     *     multipleOf2(32);   // => true
     *     multipleOf2(13);   // => false
     *
     * Note: Make sure you handle ALL the cases!
     *
     * @param num a 32-bit int. Since this is an int, it is SIGNED!
     * @return true if num is a multiple of 2 else false.
     */

    boolean multipleOf2(int num) {
        return ((num & 1) == 0);
    }

    /**
     * Return true if the given number is a multiple of 8.
     *
     * Examples:
     *     multipleOf8(256); // => true
     *     multipleOf8(135); // => false
     *     multipleOf8(92);  // => false
     *     multipleOf8(88);  // => true
     *
     * Note: Make sure you handle ALL the cases!
     *
     * @param num a 32-bit int. Since this is an int, it is SIGNED!
     * @return true if num is a multiple of 8 else false.
     */

    boolean multipleOf8(int num) {
        return (num & 7) == 0;
    }

    /**
     * Return true if the given number is a power of 2.
     *
     * Examples:
     *     powerOf2(32);   // => true
     *     powerOf2(12);   // => false
     *     powerOf2(1);    // => true
     *     powerOf2(-4);   // => false (a negative power of 2 is not a power of 2)
     *
     * Note: Make sure you handle ALL the cases!
     *
     * Hint: If num is a power of 2:
     *   What is the binary representation of num?
     *   What is the binary representation of num - 1?
     *   How does it differ if num is not a power of 2?
     *
     * @param num a 32-bit int. Since this is an int, it is SIGNED!
     * @return true if num is a multiple of 2 else false.
     */
    boolean powerOf2(int num) {
        return ((num >= 1) && (((num-1) & num) == 0));
    }
}
