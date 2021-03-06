from sys import *
from fractions import *
from itertools import *
from random import *
from functools import *
from collections import *

def isqrt(n):
    if n==0: return 0
    x,y=n,(n+1)//2
    while y<x: x,y=y,(y+n//y)//2
    return x

def introot(n,r=2):
    if n<0: return None if r%2==0 else -introot(-n,r)
    if n<2: return n
    if r==2: return isqrt(n)
    lo,hi=0,n
    while lo!=hi-1:
        mid=(lo+hi)//2
        m=pow(mid,r)
        if m==n: return mid
        if m<n: lo=mid
        else: hi=mid
    return lo

def primegen():
    yield 2;yield 3;yield 5;yield 7;yield 11;yield 13;
    ps=primegen()
    p=ps.next() and ps.next()
    q,sieve,n=pow(p,2),{},13
    
    while True:
        if n not in sieve:
            if n<q: yield n
            else:
                next,step=q+2*p,2*p
                while next in sieve: next+=step
                sieve[next]=step
                p=ps.next()
                q=pow(p,2)
        else:
            step=sieve.pop(n)
            next=n+step
            while next in sieve: next+=step
            sieve[next]=step
        n+=2

def primes(n): return list(takewhile(lambda p: p<n,primegen()))
def listprod(a): return reduce(lambda x,y: x*y,a,1)


def jacobi(a, p):
    if (p%2 == 0) or (p < 0): return None # p must be a positive odd number
    if (a == 0) or (a == 1): return a
    a, t = a%p, 1
    while a != 0:
        while not a & 1:
            a /= 2
            if p & 7 in (3, 5): t *= -1
        a, p = p, a
        if (a & 3 == 3) and (p & 3) == 3: t *= -1
        a %= p
    return t if p == 1 else 0
def chain(n, u1, v1, u2, v2, d, q, m): # Used in SLPRP.  TODO: figure out what this does.
    k = q
    while m > 0:
        u2, v2, q = (u2*v2)%n, (v2*v2-2*q)%n, (q*q)%n
        if m%2 == 1:
            u1, v1 = u2*v1+u1*v2, v2*v1+u2*u1*d
            if u1%2 == 1: u1 = u1 + n
            if v1%2 == 1: v1 = v1 + n
            u1, v1, k = (u1//2)%n, (v1//2)%n, (q*k)%n
        m //= 2
    return u1, v1, k
def pfactor(n):
    s, d, q = 0, n-1, 2
    while not d & q - 1: s, q = s+1, q*2
    return s, d // (q // 2)
    
   
def sprp(n, a, s=None, d=None):
    if n%2 == 0: return False
    if (s is None) or (d is None): s, d = pfactor(n)
    x = pow(a, d, n)
    if x == 1: return True
    for i in range(s):
        if x == n - 1: return True
        x = pow(x, 2, n)
    return False
    
    
def nextprime(n):
    if n<2: return 2
    if n==2: return 3
    n=(n+1)|1
    m=n%6
    if m==3:
        if isprime(n+2): return n+2
        n+=4
    if m==5:
        if isprime(n): return n
        n+=2
    for m in count(n,6):
        if isprime(m): return m
        if isprime(m+4): return m+4
def isprime(n, tb=(3,5,7,11), eb=(2,), mrb=()):      # TODO: more streamlining
    # tb: trial division basis
    # eb: Euler's test basis
    # mrb: Miller-Rabin basis
 
    # This test suite's first false positve is unknown but has been shown to be greater than 2**64.
    # Infinitely many are thought to exist.
 
    if n%2 == 0 or n < 13 or n == pow(isqrt(n),2): return n in (2, 3, 5, 7, 11) # Remove evens, squares, and numbers less than 13
    if any(n%p == 0 for p in tb): return n in tb                            # Trial division
    for b in eb: # Euler's test
        if b >= n: continue
        if not pow(b, n-1, n) == 1: return False
        r = n - 1
        while r%2 == 0: r //= 2
        c = pow(b, r, n)
       
        if c == 1: continue
        while c != 1 and c != n-1: c = pow(c, 2, n)
        if c == 1: return False
    s, d = pfactor(n)
    if not sprp(n, 2, s, d): return False
    if n < 2047: return True
    if n >= 3825123056546413051: # BPSW has two phases: SPRP with base 2 and SLPRP.  We just did the SPRP; now we do the SLPRP:
        d = 5
        while True:
            if gcd(d, n) > 1:
                p, q = 0, 0
                break
            if jacobi(d, n) == -1:
                p, q = 1, (1 - d) // 4
                break
            d = -d - 2*d//abs(d)
        if p == 0: return n == d
        s, t = pfactor(n + 2)
        u, v, u2, v2, m = 1, p, 1, p, t//2
        k = q
        while m > 0:
            u2, v2, q = (u2*v2)%n, (v2*v2-2*q)%n, (q*q)%n
            if m%2 == 1:
                u, v = u2*v+u*v2, v2*v+u2*u*d
                if u%2 == 1: u += n
                if v%2 == 1: v += n
                u, v, k = (u//2)%n, (v//2)%n, (q*k)%n
            m //= 2
        if (u == 0) or (v == 0): return True
        for i in range(1, s):
            v, k = (v*v-2*k)%n, (k*k)%n
            if v == 0: return True
        return False
 
    if not mrb:
        if   n <             1373653: mrb = [3]
        elif n <            25326001: mrb = [3,5]
        elif n <          3215031751: mrb = [3,5,7]
        elif n <       2152302898747: mrb = [3,5,7,11]
        elif n <       3474749660383: mrb = [3,5,6,11,13]
        elif n <     341550071728321: mrb = [3,5,7,11,13,17]   # This number is also a false positive for primes(19+1).
        elif n < 3825123056546413051: mrb = [3,5,7,11,13,17,19,23]   # Also a false positive for primes(31+1).
    return all(sprp(n, b, s, d) for b in mrb)                               # Miller-Rabin

def ilog(x, b): # greatest integer l such that b**l <= x.
    l = 0
    while x >= b:
        x //= b
        l += 1
    return l

def ispower(n):
    for p in primegen():
        r = introot(n, p)
        if r is None: continue
        if r ** p == n: return r
        if r == 1: return 0
        
def pollardRho_brent(n):
    if isprime(n): return n
    g = n
    while g == n:
        y, c, m, g, r, q = randrange(1, n), randrange(1, n), randrange(1, n), 1, 1, 1
        while g==1:
            x, k = y, 0
            for i in range(r): y = (y**2 + c) % n
            while k < r and g == 1:
                ys = y
                for i in range(min(m, r-k)):
                    y = (y**2 + c) % n
                    q = q * abs(x-y) % n
                g, k = gcd(q, n), k+m
            r *= 2
        if g==n:
            while True:
                ys = (ys**2+c)%n
                g = gcd(abs(x-ys), n)
                if g > 1: break
    return g
def pollard_pm1(n, B1=100, B2=1000):       # TODO: What are the best default bounds and way to increment them?
    if isprime(n): return n
    m = ispower(n)
    if m: return m
    while True:
        pg = primegen()
        q = 2           # TODO: what about other initial values of q?
        p = pg.next()
        while p <= B1: q, p = pow(q, p**ilog(B1, p), n), pg.next()
        g = gcd(q-1, n)
        if 1 < g < n: return g
        while p <= B2: q, p = pow(q, p, n), pg.next()
        g = gcd(q-1, n)
        if 1 < g < n: return g
        # These bounds failed.  Increase and try again.
        B1 *= 10
        B2 *= 10
def mlucas(v, a, n):
    """ Helper function for williams_pp1().  Multiplies along a Lucas sequence modulo n. """
    v1, v2 = v, (v**2 - 2) % n
    for bit in bin(a)[3:]: v1, v2 = ((v1**2 - 2) % n, (v1*v2 - v) % n) if bit == "0" else ((v1*v2 - v) % n, (v2**2 - 2) % n)
    return v1

def williams_pp1(n):
    if isprime(n): return n
    m = ispower(n)
    if m: return m
    for v in count(1):
        for p in primegen():
            e = ilog(isqrt(n), p)
            if e == 0: break
            for _ in range(e): v = mlucas(v, p, n)
            g = gcd(v - 2, n)
            if 1 < g < n: return g
            if g == n: break
def ecadd(p1, p2, p0, n): # Add two points p1 and p2 given point P0 = P1-P2 modulo n
    x1,z1 = p1; x2,z2 = p2; x0,z0 = p0
    t1, t2 = (x1-z1)*(x2+z2), (x1+z1)*(x2-z2)
    return (z0*pow(t1+t2,2,n) % n, x0*pow(t1-t2,2,n) % n)
def ecdub(p, A, n): # double point p on A modulo n
    x, z = p; An, Ad = A
    t1, t2 = pow(x+z,2,n), pow(x-z,2,n)
    t = t1 - t2
    return (t1*t2*4*Ad % n, (4*Ad*t2 + t*An)*t % n)
def ecmul(m, p, A, n): # multiply point p by m on curve A modulo n
    if m == 0: return (0, 0)
    elif m == 1: return p
    else:
        q = ecdub(p, A, n)
        if m == 2: return q
        b = 1
        while b < m: b *= 2
        b //= 4
        r = p
        while b:
            if m&b: q, r = ecdub(q, A, n), ecadd(q, r, p, n)
            else:   q, r = ecadd(r, q, p, n), ecdub(r, A, n)
            b //= 2
        return r
def ecm(n, B1=10, B2=20):       # TODO: Determine the best defaults for B1 and B2 and the best way to increment them and iters
    # "Modern" ECM using Montgomery curves and an algorithm analogous to the two-phase variant of Pollard's p-1 method
    # TODO: We currently compute the prime lists from the sieve as we need them, but this means that we recompute them at every
    #       iteration.  While it would not be particularly efficient memory-wise, we might be able to increase time-efficiency
    #       by computing the primes we need ahead of time (say once at the beginning and then once each time we increase the
    #       bounds) and saving them in lists, and then iterate the inner while loops over those lists.
    if isprime(n): return n
    m = ispower(n)
    if m: return m
    iters = 1
    while True:
        for _ in range(iters):     # TODO: multiprocessing?
            # TODO: Do we really want to call the randomizer?  Why not have seed be a function of B1, B2, and iters?
            # TODO: Are some seeds better than others?
            seed = randrange(6, n)
            u, v = (seed**2 - 5) % n, 4*seed % n
            p = pow(u, 3, n)
            Q, C = (pow(v-u,3,n)*(3*u+v) % n, 4*p*v % n), (p, pow(v,3,n))
            pg = primegen()
            p = pg.next()
            while p <= B1: Q, p = ecmul(p**ilog(B1, p), Q, C, n), pg.next()
            g = gcd(Q[1], n)
            if 1 < g < n: return g
            while p <= B2:
                # "There is a simple coding trick that can speed up the second stage. Instead of multiplying each prime times Q,
                # we iterate over i from B1 + 1 to B2, adding 2Q at each step; when i is prime, the current Q can be accumulated
                # into the running solution. Again, we defer the calculation of the greatest common divisor until the end of the
                # iteration."                                                TODO: Implement this trick and compare performance.
                Q = ecmul(p, Q, C, n)
                g *= Q[1]
                g %= n
                p = pg.next()
            g = gcd(g, n)
            if 1 < g < n: return g
            # This seed failed.  Try again with a new one.
        # These bounds failed.  Increase and try again.
        B1 *= 3
        B2 *= 3
        iters *= 2
def legendre1(a, p): return ((pow(a, (p-1) >> 1, p) + 1) % p) - 1
def legendre2(a, p):                                                 # TODO: pretty sure this computes the Jacobi symbol
    if a == 0: return 0
    x, y, L = a, p, 1
    while 1:
        if x > (y >> 1):
            x = y - x
            if y & 3 == 3: L = -L
        while x & 3 == 0: x >>= 2
        if x & 1 == 0:
            x >>= 1
            if y & 7 == 3 or y & 7 == 5: L = -L
        if x == 1: return ((L+1) % p) - 1
        if x & 3 == 3 and y & 3 == 3: L = -L
        x, y = y % x, x
legendre=legendre1
def mod_sqrt(n, p):
    a = n%p
    if p%4 == 3: return pow(a, (p+1) >> 2, p)
    elif p%8 == 5:
        v = pow(a << 1, (p-5) >> 3, p)
        i = ((a*v*v << 1) % p) - 1
        return (a*v*i)%p
    elif p%8 == 1: # Shank's method
        q, e = p-1, 0
        while q&1 == 0:
            e += 1
            q >>= 1
        n = 2
        while legendre(n, p) != -1: n += 1
        w, x, y, r = pow(a, q, p), pow(a, (q+1) >> 1, p), pow(n, q, p), e
        while True:
            if w == 1: return x
            v, k = w, 0
            while v != 1 and k+1 < r:
                v = (v*v)%p
                k += 1
            if k == 0: return x
            d = pow(y, 1 << (r-k-1), p)
            x, y = (x*d)%p, (d*d)%p
            w, r = (w*y)%p, k
    else: return a # p == 2

# modular inverse of a mod m
def modinv(a, m):
    a, x, u = a%m, 0, 1
    while a: x, u, m, a = u, x - (m/a)*u, a, m%a
    return x
def mpqs(n):
    # When the bound proves insufficiently large, we throw out all our work and start over.
    # TODO: When this happens, get more data, but don't trash what we already have.
    # TODO: Rewrite to get a few more relations before proceeding to the linear algebra.
    # TODO: When we need to increase the bound, what is the optimal increment?
    
    # Special cases: this function poorly handles primes and perfect powers:
    m = ispower(n)
    if m: return m
    if isprime(n): return n
    
    root_n, root_2n = isqrt(n), isqrt(2*n)
    bound = ilog(n**6, 10)**2  # formula chosen by experiment
    
    while True:
        try:
            prime, mod_root, log_p, num_prime = [], [], [], 0
            
            # find a number of small primes for which n is a quadratic residue
            p = 2
            while p < bound or num_prime < 3:
                leg = legendre(n%p, p)
                if leg == 1:
                    prime += [p]
                    mod_root += [mod_sqrt(n, p)]    # the rhs was [int(mod_sqrt(n, p))].  If we get errors, put it back.
                    log_p += [log(p, 10)]
                    num_prime += 1
                elif leg == 0: return p
                p = nextprime(p)
            
            x_max = len(prime)*60    # size of the sieve
            
            m_val = (x_max * root_2n) >> 1    # maximum value on the sieved range
            
            # fudging the threshold down a bit makes it easier to find powers of primes as factors
            # as well as partial-partial relationships, but it also makes the smoothness check slower.
            # there's a happy medium somewhere, depending on how efficient the smoothness check is
            thresh = log(m_val, 10) * 0.735
            
            # skip small primes. they contribute very little to the log sum
            # and add a lot of unnecessary entries to the table
            # instead, fudge the threshold down a bit, assuming ~1/4 of them pass
            min_prime = mpz(thresh*3)
            fudge = sum(log_p[i] for i,p in enumerate(prime) if p < min_prime)/4
            thresh -= fudge
            
            smooth, used_prime, partial = [], set(), {}
            num_smooth, num_used_prime, num_partial, num_poly, root_A = 0, 0, 0, 0, isqrt(root_2n // x_max)
            
            while num_smooth <= num_used_prime:
                # find an integer value A such that:
                # A is =~ sqrt(2*n) / x_max
                # A is a perfect square
                # sqrt(A) is prime, and n is a quadratic residue mod sqrt(A)
                while True:
                    root_A = nextprime(root_A)
                    leg = legendre(n, root_A)
                    if leg == 1: break
                    elif leg == 0: return root_A
                
                A = root_A**2
                
                # solve for an adequate B
                # B*B is a quadratic residue mod n, such that B*B-A*C = n
                # this is unsolvable if n is not a quadratic residue mod sqrt(A)
                b = mod_sqrt(n, root_A)
                B = (b + (n - b*b) * modinv(b + b, root_A))%A
                C = (B*B - n) // A        # B*B-A*C = n <=> C = (B*B-n)/A
                
                num_poly += 1
                
                # sieve for prime factors
                sums, i = [0.0]*(2*x_max), 0
                for p in prime:
                    if p < min_prime:
                        i += 1
                        continue
                    logp = log_p[i]
                    inv_A = modinv(A, p)
                    # modular root of the quadratic
                    a, b, k = mpz(((mod_root[i] - B) * inv_A)%p), mpz(((p - mod_root[i] - B) * inv_A)%p), 0
                    while k < x_max:
                        if k+a < x_max: sums[k+a] += logp
                        if k+b < x_max: sums[k+b] += logp
                        if k:
                            sums[k-a+x_max] += logp
                            sums[k-b+x_max] += logp
                        k += p
                    i += 1
                
                # check for smooths
                i = 0
                for v in sums:
                    if v > thresh:
                        x, vec, sqr = x_max-i if i > x_max else i, set(), []
                        # because B*B-n = A*C
                        # (A*x+B)^2 - n = A*A*x*x+2*A*B*x + B*B - n
                        #               = A*(A*x*x+2*B*x+C)
                        # gives the congruency
                        # (A*x+B)^2 = A*(A*x*x+2*B*x+C) (mod n)
                        # because A is chosen to be square, it doesn't need to be sieved
                        val = sieve_val = (A*x + 2*B)*x + C
                        if sieve_val < 0: vec, sieve_val = {-1}, -sieve_val
                        
                        for p in prime:
                            while sieve_val%p == 0:
                                if p in vec: sqr += [p] # track perfect sqr facs to avoid sqrting something huge at the end
                                vec ^= {p}
                                sieve_val = mpz(sieve_val // p)
                        if sieve_val == 1: # smooth
                            smooth += [(vec, (sqr, (A*x+B), root_A))]
                            used_prime |= vec
                        elif sieve_val in partial:
                            # combine two partials to make a (xor) smooth
                            # that is, every prime factor with an odd power is in our factor base
                            pair_vec, pair_vals = partial[sieve_val]
                            sqr += list(vec & pair_vec) + [sieve_val]
                            vec ^= pair_vec
                            smooth += [(vec, (sqr + pair_vals[0], (A*x+B)*pair_vals[1], root_A*pair_vals[2]))]
                            used_prime |= vec
                            num_partial += 1
                        else: partial[sieve_val] = (vec, (sqr, A*x+B, root_A))      # save partial for later pairing
                    i += 1
                
                num_smooth, num_used_prime = len(smooth), len(used_prime)
            
            used_prime = sorted(list(used_prime))
            
            # set up bit fields for gaussian elimination
            masks, mask, bitfields = [], 1, [0]*num_used_prime
            for vec, vals in smooth:
                masks += [mask]
                i = 0
                for p in used_prime:
                    if p in vec: bitfields[i] |= mask
                    i += 1
                mask <<= 1
            
            # row echelon form
            offset = 0
            null_cols = []
            for col in range(num_smooth):
                pivot = bitfields[col-offset] & masks[col] == 0 # This occasionally throws IndexErrors.
                # TODO: figure out why it throws errors and fix it.
                for row in range(col+1-offset, num_used_prime):
                    if bitfields[row] & masks[col]:
                        if pivot: bitfields[col-offset], bitfields[row], pivot = bitfields[row], bitfields[col-offset], False
                        else: bitfields[row] ^= bitfields[col-offset]
                if pivot:
                    null_cols += [col]
                    offset += 1
            
            # reduced row echelon form
            for row in range(num_used_prime):
                mask = bitfields[row] & -bitfields[row]        # lowest set bit
                for up_row in range(row):
                    if bitfields[up_row] & mask: bitfields[up_row] ^= bitfields[row]
            
            # check for non-trivial congruencies
            # TODO: if none exist, check combinations of null space columns...
            # if _still_ none exist, sieve more values
            for col in null_cols:
                all_vec, (lh, rh, rA) = smooth[col]
                lhs = lh   # sieved values (left hand side)
                rhs = [rh] # sieved values - n (right hand side)
                rAs = [rA] # root_As (cofactor of lhs)
                i = 0
                for field in bitfields:
                    if field & masks[col]:
                        vec, (lh, rh, rA) = smooth[i]
                        lhs += list(all_vec & vec) + lh
                        all_vec ^= vec
                        rhs += [rh]
                        rAs += [rA]
                    i += 1
                factor = gcd(listprod(rAs)*listprod(lhs) - listprod(rhs), n)
                if 1 < factor < n: return factor
        
        except IndexError: pass
        
        bound *= 1.2

def primefac(n, trial_limit=1000, rho_rounds=42000, verbose=False,
             methods=(pollardRho_brent, pollard_pm1, williams_pp1, ecm, mpqs)):
    # Obtains a complete factorization of n, yielding the prime factors as they are obtained.
    # If the user explicitly specifies a splitting method, use that method.  Otherwise,
    # 1.  Pull out small factors with trial division.
    # TODO: a few rounds of Fermat's method?
    # 2.  Do a few rounds of Pollard's Rho algorithm.
    # TODO: a few rounds of ECM by itself?
    # TODO: a certain amount of P-1?
    # 3.  Launch multifactor on the remainder.  Multifactor has enough overhead that we want to be fairly sure that rho isn't
    #     likely to yield new factors soon.  The default value of rho_rounds=42000 seems good for that but is probably overkill.
    
    if n < 2: return
    if isprime(n): yield n; return
    
    factors, nroot = [], isqrt(n)
    for p in primegen(): # Note that we remove factors of 2 whether the user wants to or not.
        if n%p == 0:
            while n%p == 0:
                yield p
                n //= p
            nroot = isqrt(n)
            if isprime(n):
                yield n
                return
        if p > nroot:
            if n != 1: yield n
            return
        if p >= trial_limit: break
    if isprime(n): yield n; return
    
    if rho_rounds == "inf":
        factors = [n]
        while len(factors) != 0:
            n = min(factors)
            factors.remove(n)
            f = pollardRho_brent(n)
            if isprime(f): yield f
            else: factors.append(f)
            n //= f
            if isprime(n): yield n
            else: factors.append(n)
        return
    
    factors, difficult = [n], []
    while len(factors) != 0:
        rhocount = 0
        n = factors.pop()
        try:
            g = n
            while g == n:
                x, c, g = randrange(1, n), randrange(1, n), 1
                y = x
                while g==1:
                    if rhocount >= rho_rounds: raise Exception
                    rhocount += 1
                    x = (x**2 + c) % n
                    y = (y**2 + c) % n
                    y = (y**2 + c) % n
                    g = gcd(x-y, n)
            # We now have a nontrivial factor g of n.  If we took too long to get here, we're actually at the except statement.
            if isprime(g): yield g
            else: factors.append(g)
            n //= g
            if isprime(n): yield n
            else: factors.append(n)
        except Exception: difficult.append(n) # Factoring n took too long.  We'll have multifactor chug on it.
    
    factors = difficult
    while len(factors) != 0:
        n = min(factors)
        factors.remove(n)
        f = multifactor(n, methods=methods, verbose=verbose)
        if isprime(f): yield f
        else: factors.append(f)
        n //= f
        if isprime(n): yield n
        else: factors.append(n)

def divisors(factors):
    div = [1]
    
    for (p, r) in Counter(factors).items():
        div = [d * pow(p,e) for d in div for e in range(r + 1)]
    return sorted(div)

def phi(n):
    for k,v in Counter(primefac(n,methods=mpqs)).iteritems():
        n=n//k*(k-1)
    return n

