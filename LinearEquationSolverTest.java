import org.junit.Test;
import static org.junit.Assert.*;

public class LinearEquationSolverTest {

    @Test
    public void testSolveLinearEquations() {
        assertSolveLinearEquations(new double[][]{{3, 2, 0}, {1, -1, 0}, {0, 5, 1}}, new double[]{2, 4, -1}, new double[]{2, -2, 9});
        assertSolveLinearEquations(new double[][]{{1, 0, 0}, {1, 0, 0}, {1, 0, 0}}, new double[]{3, 4, 5}, "ERROR: Cannot find solution.");
        assertSolveLinearEquations(new double[][]{{1, 0, 0}, {0, 1, 0}, {0, 0, 1}}, new double[]{3, 4, 5}, new double[]{3, 4, 5});
        assertSolveLinearEquations(new double[][]{{1, 1}, {2, -1}}, new double[]{24, -6}, new double[]{6, 18});
        assertSolveLinearEquations(new double[][]{{1, 0}, {2, 0}, {3, 1}}, new double[]{3, 6, 10}, "ERROR: Cannot find solution.");
        assertSolveLinearEquations(new double[][]{{2, 0}, {3, 1}}, new double[]{6, 10}, new double[]{3, 1});
        assertSolveLinearEquations(new double[][]{{1}, {2}}, new double[]{3, 6}, "ERROR: Cannot find solution.");
        assertSolveLinearEquations(new double[][]{{1, 0, 0}, {2, 0, 0}, {3, 1, 0}}, new double[]{3, 6, 10}, "ERROR: Cannot find solution.");
        assertSolveLinearEquations(new double[][]{{1, 0}, {2, 0}}, new double[]{3, 6}, "ERROR: Cannot find solution.");
        assertSolveLinearEquations(new double[][]{{1, 0, 1}, {2, 0, 0}, {3, 1, 0}}, new double[]{3, 6, 10}, new double[]{3, 1, 0});
    }

    private void assertSolveLinearEquations(double[][] a, double[] b, Object expectedOutput) {
        try {
            double[] result = LinearEquationSolver.solveLinearEquations(a, b);
            assertArrayEquals((double[]) expectedOutput, result, 0.01);
        } catch (IllegalArgumentException e) {
            assertEquals(expectedOutput, e.getMessage());
        }
    }
}
