def convertir_a_romano(n):
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]
        romano = ''
        i = 0
        while n > 0:
            for _ in range(n // val[i]):
                romano += syb[i]
                n -= val[i]
            i += 1
        return romano