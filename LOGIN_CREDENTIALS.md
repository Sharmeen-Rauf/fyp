# 🔐 Login Credentials Guide

## No Default Credentials

**The system does NOT have default login credentials.** You need to create an account first.

---

## ✅ **Option 1: Register a New Account** (Recommended)

1. **Go to Register Page:**
   - Click "Don't have an account? Sign Up" on the login page
   - Or visit: `http://localhost:3000/register` (local) or `https://your-vercel-url.vercel.app/register` (deployed)

2. **Fill in the form:**
   - **Full Name**: Your name
   - **Email**: Your email address
   - **Password**: Choose a secure password
   - **Role**: Select one:
     - `candidate` - For job applicants
     - `hr` - For HR managers
     - `admin` - For administrators

3. **Click "Sign Up"**

4. **Login** with your new credentials

---

## ✅ **Option 2: Create Default Admin User** (For Testing)

If you want a quick default admin account for testing:

### **Step 1: Run the script**

```bash
cd backend
python create_default_user.py
```

### **Step 2: Login with default credentials**

- **Email**: `admin@botboss.com`
- **Password**: `admin123`

⚠️ **Important**: Change this password after first login!

---

## 📝 **Example Test Accounts**

You can create multiple accounts for testing:

### **HR Account:**
- Email: `hr@botboss.com`
- Password: `hr123`
- Role: `hr`

### **Candidate Account:**
- Email: `candidate@botboss.com`
- Password: `candidate123`
- Role: `candidate`

### **Admin Account:**
- Email: `admin@botboss.com`
- Password: `admin123`
- Role: `admin`

---

## 🔧 **Using API to Create User**

You can also create users via API:

### **Using Swagger UI:**
1. Visit: `http://localhost:8000/docs`
2. Go to `/api/v1/users/register` endpoint
3. Click "Try it out"
4. Enter user data:
```json
{
  "email": "test@example.com",
  "password": "password123",
  "full_name": "Test User",
  "role": "candidate"
}
```
5. Click "Execute"

### **Using cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "role": "candidate"
  }'
```

---

## 🚨 **Troubleshooting**

### **"Incorrect email or password"**
- Make sure you registered first
- Check that email and password are correct
- Ensure backend is running

### **"Email already registered"**
- The email is already in use
- Try a different email or login with existing account

### **Can't access register page**
- Make sure frontend is running
- Check the URL is correct
- Try: `http://localhost:3000/register`

---

## 💡 **Quick Start**

1. **First time?** → Register a new account
2. **Need admin?** → Run `python backend/create_default_user.py`
3. **Testing?** → Create multiple accounts with different roles

---

## 📍 **Where to Register**

- **Local**: `http://localhost:3000/register`
- **Deployed**: `https://your-vercel-url.vercel.app/register`

