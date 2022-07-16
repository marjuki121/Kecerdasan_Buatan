def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class Permintaan():
    minimum = 500
    maximum = 3000

    def turun(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

class Persediaan():
    sedikit = 50
    tidak_cukup = 100
    cukup = 200
    banyak= 300
    sangat_banyak = 350

    def sedikit(self, x):
        if x >= self.tidak_cukup:
            return 0
        elif x <= self.cukup:
            return 1
        else:
            return down(x, self.cukup, self.tidak_cukup)
    
    def tidak_cukup(self, x):
        if self.cukup < x < self.banyak:
            return up(x, self.cukup, self.tidak_cukup)
        elif self.cukup < x < self.banyak:
            return down(x, self.tidak_cukup, self.banyak)
        elif x == self.tidak_cukup:
            return 1
        else:
            return 0

    def cukup(self, x):
        if self.banyak < x < self.cukup:
            return up(x, self.banyak, self.cukup)
        elif self.cukup < x < self.sangat_banyak:
            return down(x, self.cukup, self.sangat_banyak)
        elif x == self.cukup:
            return 1
        else:
            return 0

    def banyak(self, x):
        if self.sangat_banyak < x < self.banyak:
            return up(x, self.sangat_banyak, self.banyak)
        elif self.banyak < x < self.sangat_banyak:
            return down(x, self.banyak, self.sangat_banyak)
        elif x == self.banyak:
            return 1
        else:
            return 0

    def sangat_banyak(self, x):
        if x >= self.sangat_banyak:
            return 1
        elif x <= self.cukup:
            return 0
        else:
            return up(x, self.cukup, self.sangat_banyak)

class Produksi():
    minimum = 1000
    maximum = 4000
    
    def kurang(self, α):
        return self.maximum - α * (self.maximum-self.minimum)

    def tambah(self, α):
        return α *(self.maximum - self.minimum) + self.minimum

    # 2 permintaan 5 persediaan
    def inferensi(self, jumlah_permintaan, jumlah_persediaan):
        pmt = Permintaan()
        psd = Persediaan()
        result = []
        # [R1] JIKA permintaan turun, dan persediaan sangat banyak, MAKA
        # produksi barang berkurang.
        α1 = min(pmt.turun(jumlah_permintaan), psd.sangat_banyak(jumlah_persediaan))
        z1 = self.kurang(α1)
        result.append((α1, z1))
        # [R2] JIKA permintaan turun, dan persediaan sedikit, MAKA
        # produksi barang berkurang.
        α2 = min(pmt.turun(jumlah_permintaan), psd.sedikit(jumlah_persediaan))
        z2 = self.kurang(α2)
        result.append((α2, z2))
        # [R3] JIKA permintaan naik, dan persediaan sangat banyak, MAKA
        # produksi barang bertambah.
        α3 = min(pmt.naik(jumlah_permintaan), psd.sangat_banyak(jumlah_persediaan))
        z3 = self.tambah(α3)
        result.append((α3, z3))
        # [R4] JIKA permintaan naik, dan persediaan sedikit, MAKA
        # produksi barang bertambah.
        α4 = min(pmt.naik(jumlah_permintaan), psd.sedikit(jumlah_persediaan))
        z4 = self.tambah(α4)
        result.append((α4, z4))
        # [R5] JIKA permintaan naik, dan persediaan cukup, MAKA
        # produksi barang bertambah.
        α5 = min(pmt.naik(jumlah_permintaan), psd.cukup(jumlah_persediaan))
        z5 = self.tambah(α5)
        result.append((α5, z5))
        # [R6] JIKA permintaan turun, dan persediaan cukup, MAKA
        # produksi barang berkurang.
        α6 = min(pmt.turun(jumlah_permintaan), psd.cukup(jumlah_persediaan))
        z6 = self.kurang(α6)
        result.append((α6, z6))
        # [R7] JIKA permintaan turun, dan persediaan tidak cukup, MAKA
        # produksi barang bertambah.
        α7 = min(pmt.turun(jumlah_permintaan), psd.tidak_cukup(jumlah_persediaan))
        z7 = self.tambah(α7)
        result.append((α7, z7))
        # [R8] JIKA permintaan naik, dan persediaan tidak cukup, MAKA
        # produksi barang bertambah.
        α8 = min(pmt.naik(jumlah_permintaan), psd.tidak_cukup(jumlah_persediaan))
        z8 = self.tambah(α8)
        result.append((α8, z8))
        # [R9] JIKA permintaan turun, dan persediaan banyak, MAKA
        # produksi barang berkurang.
        α9 = min(pmt.turun(jumlah_permintaan), psd.banyak(jumlah_persediaan))
        z9 = self.kurang(α9)
        result.append((α9, z9))
        # [R10] JIKA permintaan turun, dan persediaan banyak, MAKA
        # produksi barang bertambah.
        α10 = min(pmt.turun(jumlah_permintaan), psd.banyak(jumlah_persediaan))
        z10 = self.tambah(α10)
        result.append((α10, z10))

        return result
    
    def defuzifikasi(self, jumlah_permintaan, jumlah_persediaan):
        inferensi_values = self.inferensi(jumlah_permintaan, jumlah_persediaan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])