package com.prj2;

/**
 * LeetCode 733. Гүехэн хайлт (BFS): нүдийг дараалалд оруулахдаа өнгийг нь сольдог тул нүд бүр
 * нэг удаа орно. Θ(R·C) хугацаа, дараалал Θ(R·C) санах ой (нүдийг r·C + c гэж int-ээр кодолно).
 */
public class FloodFill {

    private static final int[] DR = {-1, 1, 0, 0};
    private static final int[] DC = {0, 0, -1, 1};

    public int[][] floodFill(int[][] image, int sr, int sc, int color) {
        int old = image[sr][sc];
        if (old == color) return image;
        int rows = image.length;
        int cols = image[0].length;
        int[] queue = new int[rows * cols];
        int head = 0;
        int tail = 0;
        image[sr][sc] = color;
        queue[tail++] = sr * cols + sc;
        while (head < tail) {
            int cell = queue[head++];
            int r = cell / cols;
            int c = cell % cols;
            for (int d = 0; d < 4; d++) {
                int nr = r + DR[d];
                int nc = c + DC[d];
                if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && image[nr][nc] == old) {
                    image[nr][nc] = color;
                    queue[tail++] = nr * cols + nc;
                }
            }
        }
        return image;
    }
}
