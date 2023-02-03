public class BitVector
{
    /**
     * 32-bit data initialized to all zeros. Here is what you will be using to
     * represent the Bit Vector. Do not change its scope from private.
     */
    private int bits;

    /** You may not add any more fields to this class other than the given one. */

    /**
     * Sets the bit (sets to 1) pointed to by index.
     * @param index index of which bit to set.
     *              0 for the least significant bit (right most bit).
     *              31 for the most significant bit.
     */
    public void set(int index) {
        this.bits = this.bits | (1 << index);
    }

    /**
     * Clears the bit (sets to 0) pointed to by index.
     * @param index index of which bit to set.
     *              0 for the least significant bit (right most bit).
     *              31 for the most significant bit.
     */
    public void clear(int index) {
        this.bits = this.bits & ~(1 << index);
    }

    /**
     * Toggles the bit (sets to the opposite of its current value) pointed to by
     * index.
     * @param index index of which bit to set.
     *              0 for the least significant bit (right most bit).
     *              31 for the most significant bit.
     */
    public void toggle(int index) {
        this.bits = this.bits ^ (1 << index);
    }

    /**
     * Returns true if the bit pointed to by index is currently set.
     * @param index index of which bit to check.
     *              0 for the least significant bit (right-most bit).
     *              31 for the most significant bit.
     * @return true if the bit is set, false if the bit is clear.
     *         If the index is out of range (index >= 32), then return false.
     */
    public boolean isSet(int index) {
        return (!(index >= 32) && ((1 << index) == (this.bits & (1 << index))));
    }

    /**
     * Returns true if the bit pointed to by index is currently clear.
     * @param index index of which bit to check.
     *              0 for the least significant bit (right-most bit).
     *              31 for the most significant bit.
     * @return true if the bit is clear, false if the bit is set.
     *         If the index is out of range (index >= 32), then return true.
     */
    public boolean isClear(int index) {
        return ((index >= 32) || ((1 << index) != (this.bits & (1 << index))));
    }

    /**
     * Returns the number of bits currently set (=1) in this bit vector.
     * You may use the ++ operator to increment your counter.
     */
    public int onesCount() {
        int cnt = 0;
        for (int i = 0; i < 32; i++) {
            if ((this.bits & (1 << i)) != 0) {
                cnt++;
            }
        }
        return cnt;
    }

    /**
     * Returns the number of bits currently clear (=0) in this bit vector.
     * You may use the ++ operator to increment your counter.
     */
    public int zerosCount() {
        int cnt = 0;
        for (int i = 0; i < 32; i++) {
            if ((this.bits & (1 << i)) == 0) {
                cnt++;
            }
        }
        return cnt;
    }

    /**
     * Returns the "size" of this BitVector. The size of this bit vector is
     * defined to be the minimum number of bits that will represent all of the
     * ones.
     *
     * For example, the size of the bit vector 00010000 will be 5.
     */
    public int size() {
        int size = 0;
        for (int i = 31; i >= 0; i--) {
            if ((this.bits & (1 << i)) != 0) {
                return (i + 1);
            }
        }
        return 1;
    }
}