# NUJ Uttar Pradesh — Complete Usage Guide

**National Union of Journalists (Uttar Pradesh)** · Django Web Application

---

## 🚀 Start the Server

**Double-click `start_dev.bat`** — does everything automatically.

| URL | Page |
|---|---|
| http://localhost:8000/ | Homepage |
| http://localhost:8000/nuj-admin/ | Admin Panel |
| http://localhost:8000/about/ | About NUJ UP |
| http://localhost:8000/city-units/ | All 75 City Units |
| http://localhost:8000/office-bearers/ | UP Office Bearers |
| http://localhost:8000/membership/login/ | Member Login |
| http://localhost:8000/membership/portal/ | Member Dashboard |
| http://localhost:8000/membership/apply/ | Apply for Membership |
| http://localhost:8000/membership/status/ | Track Application |

**Admin:** http://localhost:8000/nuj-admin/ — Login: `admin` / `admin123`  
**Contact:** 7054000149

---

## 📸 HOW TO ADD PHOTOS

### Adding a Photo to an Office Bearer
1. Go to **Admin → People → Office Bearers**
2. Click the bearer's name
3. Scroll to **📸 Photo & Bio** section
4. Click **"Choose File"** → select photo → click **Save**
5. The photo shows on homepage and office bearers page automatically

### Adding a Photo to a City Unit Member
1. Go to **Admin → People → City Units**
2. Click the city unit name
3. Scroll to the **"City Unit Members"** section at the bottom
4. For each member, click **"Choose File"** under Photo
5. Click **Save**

### Adding a Profile Photo to a Member (Portal)
1. Go to **Admin → Membership → Member Profiles**
2. Click the member
3. Upload photo in **📸 Photo** section → Save

---

## 🏙 HOW TO ADD A CITY UNIT

1. Go to **Admin → People → City Units → Add City Unit**
2. Fill in:
   - **Name**: e.g., "NUJ Kanpur City Unit"
   - **City**: Select from 75 UP districts dropdown
   - **Established Year**, **Member Count**
   - **Phone**, **Email**, **Address**
   - **Cover Image** (optional photo for the unit page)
3. In **City Unit Members** section below, add:
   - **President**: Name, Role="President", Photo, Phone, Email
   - **Secretary**: Name, Role="Secretary", Photo, Phone, Email
   - **Vice President**, **Treasurer**, etc.
4. Check **"Published"** → Click **Save**

> **Note:** President, Secretary, Treasurer and Convener automatically get **large cards with photos** on the city unit page. All others appear in a compact list.

---

## 👥 HOW TO ADD UP-LEVEL OFFICE BEARERS

1. Go to **Admin → People → Office Bearers → Add**
2. Fill in:
   - **Name**, **Role** (e.g., "President"), **Category** (select from dropdown)
   - **State**: Select the bearer's home city
   - **Photo**: Upload a portrait photo
   - **Bio**: Short biography
   - **Email**, **Phone** (check "Show Contact" to display publicly)
3. Check **Featured on Homepage** to show on the homepage leadership strip
4. Check **Published** → Save

---

## 📰 HOW TO PUBLISH NEWS / PRESS RELEASES

**News:**
1. **Admin → Newsroom → News Posts → Add**
2. Title → slug auto-fills → pick Category → write Summary + Body
3. Upload Cover Image → set Published date → check **Published** → Save

**Press Releases:**
1. **Admin → Newsroom → Press Releases → Add**
2. Title → Summary → Body → optionally attach PDF
3. Check **Published** → Save

---

## ✅ MEMBERSHIP APPROVAL WORKFLOW

1. Someone fills the form at `/membership/apply/`
2. You see it in **Admin → Membership → Membership Applications** (Status: Submitted)
3. Open it → check all details, view ID proof and press card
4. Change **Status** → `Approved` → Save
5. Back in the list → select the application → Action: **"✅ Create member login accounts for approved"** → Go
6. System creates a username (from their email) + temporary account
7. Tell the member their username and that they can log in at `/membership/login/`

---

## 🔧 HOW TO UPDATE SITE SETTINGS

1. **Admin → Core → Site Settings → click the existing entry**
2. Update:
   - **Member Count**, **City Units Count** (shown in homepage stats bar)
   - **Office Address**, **Phone**, **Email**
   - **Social Media links** (Facebook, Twitter, YouTube, etc.)
   - **Logo** (upload your NUJ UP logo — appears in navbar)
   - **Favicon** (small icon in browser tab)
3. Save

---

## 📋 ALL 75 UP DISTRICTS (City Codes)

All districts are available in the City dropdown across the admin:

Agra · Aligarh · Ambedkar Nagar · Amethi · Amroha · Ayodhya · Azamgarh · Badaun · Bagpat · Bahraich · Ballia · Balrampur · Banda · Barabanki · Bareilly · Basti · Bijnor · Bulandshahr · Chandauli · Chitrakoot · Deoria · Etah · Etawah · Farrukhabad · Fatehpur · Firozabad · Gautam Buddha Nagar (Noida) · Ghaziabad · Ghazipur · Gonda · Gorakhpur · Hamirpur · Hapur · Hardoi · Hathras · Jalaun · Jaunpur · Jhansi · Kannauj · Kanpur Nagar · Kanpur Dehat · Kasganj · Kaushambi · Kheri (Lakhimpur) · Kushinagar · Lalitpur · **Lucknow** · Maharajganj · Mahoba · Mainpuri · Mathura · Mau · Meerut · Mirzapur · Moradabad · Muzaffarnagar · Pilibhit · Pratapgarh · Prayagraj · Raebareli · Rampur · Saharanpur · Sambhal · Sant Kabir Nagar · Sant Ravidas Nagar · Shahjahanpur · Shamli · Shravasti · Siddharthnagar · Sitapur · Sonbhadra · Sultanpur · Unnao · Varanasi

---

## 📁 Project Structure

```
nujindia/
├── apps/
│   ├── core/          # Site settings, announcements
│   ├── people/        # Office bearers, city units (75 districts)
│   ├── newsroom/      # News, press releases, letters, gallery
│   ├── documents/     # Circulars, notices, policy documents
│   ├── events/        # Events with speakers
│   ├── membership/    # Applications + member portal login
│   ├── contact/       # Contact form with reply-by-email
│   └── pages/         # Home, About, static pages
├── templates/         # All HTML templates
├── fixtures/          # Initial data (phone: 7054000149, 75 cities)
├── start_dev.bat      # One-click launcher
└── manage.py
```
