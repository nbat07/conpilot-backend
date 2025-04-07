public class TrianglePrinter {
    public static String printTriangle(int N) {
        StringBuilder result = new StringBuilder();for (int i = 1; i <= N; i++) {
            for (int j = 0; j < i; j++) {
                result.append("*");
            }
            result.append("\n");
        }
        return result.toString();
    }
}