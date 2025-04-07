public class TemperatureConverter {
    public static double fahrenheitToCelsius(double Fahrenheit) {
        double Celsius = (Fahrenheit - 32) * 5 / 9;
        double Celsius0 = Math.round(Celsius * 100.0);return Celsius0 / 100.0;
    }
}