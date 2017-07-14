#include "Fraction.hpp"

using namespace openshot;

Fraction::Fraction() :
	num(1), den(1)
{

}

Fraction::Fraction(int num, int den):
	num(num), den(den)
{

}

float Fraction::ToFloat(void) {
	return float(num) / float(den);
}

double Fraction::ToDouble(void) {
	return double(num) / double(den);
}

int Fraction::ToInt(void) {
	return round((float) num / den);
}

int Fraction::GreatestCommonDenominator(void) {
	int first = num;
	int second = den;

	// Find the biggest whole number that will divide into both the numerator
	// and denominator
	int t;
	while (second != 0) {
		t = second;
		second = first % second;
		first = t;
	}
	return first;

}

void Fraction::Reduce(void) {
	int GCD = GreatestCommonDenominator();
	num = num / GCD;
	den = den / GCD;
}

Fraction Fraction::Reciprocal() {
	return Fraction(den, num);
}
