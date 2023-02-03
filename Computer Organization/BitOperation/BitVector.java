public class BitVector
{
    private int bits;

    public void set(int index) {
        this.bits = this.bits | (1 << index);
    }

    public void clear(int index) {
        this.bits = this.bits & ~(1 << index);
    }

    public void toggle(int index) {
        this.bits = this.bits ^ (1 << index);
    }

    public boolean isSet(int index) {
        return (!(index >= 32) && ((1 << index) == (this.bits & (1 << index))));
    }

    public boolean isClear(int index) {
        return ((index >= 32) || ((1 << index) != (this.bits & (1 << index))));
    }

    public int onesCount() {
        int cnt = 0;
        for (int i = 0; i < 32; i++) {
            if ((this.bits & (1 << i)) != 0) {
                cnt++;
            }
        }
        return cnt;
    }

    public int zerosCount() {
        int cnt = 0;
        for (int i = 0; i < 32; i++) {
            if ((this.bits & (1 << i)) == 0) {
                cnt++;
            }
        }
        return cnt;
    }
    
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