public class Hasta {

   
    private String id;
    private String adi;
    private String soyadi;
    private String cinsiyet;
    private int yas; // 2. Yaş sayı olduğu için int yaptık
    private String yakini;
    private String sikayet; // 3. Şikayet değişkenini en üstte tanımladık

    // Yapıcı Metot (Constructor)
    public Hasta(String id, String adi, String soyadi, String cinsiyet, int yas, String yakini, String sikayet) {
        this.id = id;
        this.adi = adi;
        this.soyadi = soyadi;
        this.cinsiyet = cinsiyet;
        this.yas = yas;
        this.yakini = yakini;
        this.sikayet = sikayet; // Şikayeti de kurucuya ekledik
    }

    // Getters ve Setters kısımları (String yerine doğru veri tipleri ile)
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getFullName() { return adi + " " + soyadi; }
    
    public int getAge() { return yas; }
    public void setAge(int yas) { this.yas = yas; }

    public String getComplaint() { return sikayet; }
    public void setComplaint(String sikayet) { this.sikayet = sikayet; }

    public String getYakini() { return yakini; }
    public void setYakini(String yakini) { this.yakini = yakini; }

    // 4. toString içinde doğru değişkenleri ve metotları çağırdık
    @Override
    public String toString() {
        return "Hasta Bilgisi [TC/ID: " + id + ", İsim: " + getFullName() + ", Yaş: " + yas + ", Şikayet: " + sikayet + "]";
    }
}