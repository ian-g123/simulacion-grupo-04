W = 32
N = 624
M = 397
R = 31
A = 0x9908B0DF
U = 11
D = 0xFFFFFFFF
S = 7
B = 0x9D2C5680
T = 15
C = 0xEFC60000
L = 18
F = 1812433253
W_MASK = pow(2, W) - 1

# Genero una mascara superior y inferior
lower_mask = (
    1 << R
) - 1  # Número binario que consiste en mover un 1, R veces a la izquierda y restarle 1
upper_mask = (~lower_mask) & W_MASK


# Definimos la clase MT19937
class MersenneTwister:
    # Inicializa el generador mersenne-twister con una semilla
    # Setea el tamaño de la secuencia en N (para nuestro caso es 624)
    def __init__(self, seed):
        """
        Inicializa el generador mersenne-twister con una semilla\n
        Setea el tamaño de la secuencia en N (para nuestro caso es 624)
        """
        self.index = N
        self.state = [0] * N
        self._seed(seed)

    # Asigna los N numeros a partir de la semilla a la que se le aplica una marca, los genera combinando el numero anterior, el actual, por una constante F y a eso sumandole la posicion actual.
    def _seed(self, seed):
        self.state[0] = seed & W_MASK
        for i in range(1, N):
            self.state[i] = (
                F * (self.state[i - 1] ^ (self.state[i - 1] >> (W - 2))) + i
            ) & W_MASK

    # Genera los siguientes N numeros pseudoaleatorios, a partir del resultado de la suma de 2 numeros consecutivos a los que se les hace un par de transformaciones
    # luego se le aplica una marca XOR para finalmente combinar el resultado con otro estado M posiciones mas adelante.
    def _twist(self):
        for i in range(N):
            x = (self.state[i] & upper_mask) + \
                (self.state[(i + 1) % N] & lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= A
            self.state[i] = self.state[(i + M) % N] ^ xA
        self.index = 0

    # Extrae el siguiente numero segun el indice actual y se encarga de llamar a twist si es necesario generar una nueva secuencia de N numeros
    # Ademas aplica un par de shifteos de bits para mejorar la distribucion y el periodo.
    # El numero devuelto esta en este itnervalo [0, 2**32-1]
    def rand(self):
        if self.index >= N:
            self._twist()

        y = self.state[self.index]
        y ^= (y >> U) & D
        y ^= (y << S) & B
        y ^= (y << T) & C
        y ^= y >> L

        self.index += 1
        return y & W_MASK

    # Es una modificacion del metodo next para normalizar la salida al intervalo [0,1]
    def uniform(self):
        return self.rand() / (pow(2, W) - 1)
