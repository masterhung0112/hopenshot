#ifndef HOPENSHOT_FRACTION_H
#define HOPENSHOT_FRACTION_H

#include <math.h>

namespace openshot {
	class Fraction {
	public:
		int num;
		int den;

		Fraction();
		Fraction(int num, int den);

		int GreatestCommonDenominator();
		void Reduce();
		float ToFloat();
		double ToDouble();
		int ToInt();
		Fraction Reciprocal();
	};
}

#endif
