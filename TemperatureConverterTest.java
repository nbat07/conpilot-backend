import org.junit.Test;

import static org.junit.Assert.*;

public class TemperatureConverterTest {

    @Test
    public void testFahrenheitToCelsius() {
        assertFahrenheitToCelsius(212, 100.0);
        assertFahrenheitToCelsius(0.555, -17.47);
        assertFahrenheitToCelsius(0, -17.78);
        assertFahrenheitToCelsius(-40, -40.0);
        assertFahrenheitToCelsius(32, 0.0);
        assertFahrenheitToCelsius(373, 189.44);
        assertFahrenheitToCelsius(-23, -30.56);
        assertFahrenheitToCelsius(-40.00, -40.0);
    }

    private void assertFahrenheitToCelsius(double input, double expectedOutput) {
        assertEquals(expectedOutput, TemperatureConverter.fahrenheitToCelsius(input), 0.01);
    }
}
