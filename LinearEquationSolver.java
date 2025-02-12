import org.apache.commons.math3.linear.*;

public class LinearEquationSolver {
    public static double[] solveLinearEquations(double[][] a, double[] b) {
        try {
            RealMatrix coefficients = new Array2DRowRealMatrix(a, false);
            DecompositionSolver solver = new LUDecomposition(coefficients).getSolver();
return solver.solve(new ArrayRealVector(b, false)).toArray();
        } catch (Exception e) {
            throw new IllegalArgumentException("Invalid matrix or vector dimensions", e);
        }
    }
}