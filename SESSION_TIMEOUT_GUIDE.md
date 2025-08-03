# ⏰ Session Timeout Feature Guide - JS IT Computer Trading

## ✅ **Features Implemented**

### **1. Automatic Session Timeout**
- ✅ **20 seconds** for testing (easily configurable)
- ✅ **10 minutes** recommended for production
- ✅ **Server-side timeout** via Django middleware
- ✅ **Client-side countdown** with JavaScript

### **2. User Experience Features**
- ✅ **Warning modal** appears 10 seconds before timeout
- ✅ **Countdown timer** in warning modal
- ✅ **Activity detection** (click, keypress, mousemove, scroll)
- ✅ **Reset countdown** on any user activity
- ✅ **Graceful logout** with warning message

### **3. Security Features**
- ✅ **Server-side validation** prevents bypass
- ✅ **Session cleanup** on timeout
- ✅ **Automatic logout** after inactivity
- ✅ **Warning system** gives users chance to stay logged in

## 🔧 **How It Works**

### **Server-Side (Django Middleware):**
```python
class SessionTimeoutMiddleware:
    def __call__(self, request):
        if request.user.is_authenticated:
            # Check last activity time
            last_activity = request.session.get('last_activity')
            
            # If timeout exceeded, logout user
            if timezone.now() - last_activity > timeout_period:
                logout(request)
                return redirect('home')
            
            # Update last activity time
            request.session['last_activity'] = timezone.now().isoformat()
```

### **Client-Side (JavaScript):**
```javascript
// Countdown timer
let countdown = sessionTimeout; // 20 seconds

// Reset on user activity
document.addEventListener('click', resetCountdown);
document.addEventListener('keypress', resetCountdown);
document.addEventListener('mousemove', resetCountdown);

// Show warning 10 seconds before timeout
if (countdown <= 10) {
    showTimeoutWarning();
}
```

## ⚙️ **Configuration**

### **Current Settings (Testing):**
```python
# In settings.py
SESSION_TIMEOUT = 20  # 20 seconds for testing
```

### **Production Settings:**
```python
# In settings.py
SESSION_TIMEOUT = 600  # 10 minutes for production
```

### **Customization Options:**
- **Warning time**: Currently 10 seconds before timeout
- **Activity detection**: Click, keypress, mousemove, scroll
- **Timeout period**: Configurable in settings.py

## 🎯 **User Experience Flow**

### **1. Normal Usage:**
1. User logs in → Session starts
2. User is active → Countdown resets
3. User continues working → No timeout

### **2. Inactivity Warning:**
1. User stops activity → Countdown starts
2. 10 seconds remaining → Warning modal appears
3. User clicks "Stay Logged In" → Session continues
4. User ignores warning → Auto logout after 10 seconds

### **3. Complete Inactivity:**
1. User leaves computer → Countdown continues
2. 20 seconds total → Automatic logout
3. User returns → Must log in again

## 🛡️ **Security Benefits**

### **For Business:**
- **Prevents unauthorized access** if user leaves computer
- **Protects sensitive data** from unauthorized users
- **Compliance** with security best practices
- **Automatic cleanup** of inactive sessions

### **For Users:**
- **Clear warning** before timeout
- **Easy to stay logged in** with one click
- **Activity detection** prevents accidental timeouts
- **Graceful logout** with clear messaging

## 📊 **Testing the Feature**

### **Quick Test (20 seconds):**
1. **Login** to the system
2. **Stop all activity** (don't move mouse, click, or type)
3. **Wait 10 seconds** → Warning modal appears
4. **Wait 10 more seconds** → Auto logout

### **Activity Test:**
1. **Login** to the system
2. **Keep moving mouse** or clicking
3. **Countdown resets** on each activity
4. **No timeout** occurs while active

## 🔄 **How to Change Timeout Duration**

### **For Testing (Quick):**
```python
# In js_it_comp_trad/settings.py
SESSION_TIMEOUT = 20  # 20 seconds
```

### **For Production (Secure):**
```python
# In js_it_comp_trad/settings.py
SESSION_TIMEOUT = 600  # 10 minutes
```

### **For Custom Duration:**
```python
# In js_it_comp_trad/settings.py
SESSION_TIMEOUT = 300  # 5 minutes
SESSION_TIMEOUT = 1800  # 30 minutes
```

## 🎨 **Visual Features**

### **Warning Modal:**
- ⚠️ **Warning icon** with triangle
- 📊 **Countdown timer** showing seconds remaining
- 🔄 **"Stay Logged In"** button to continue session
- 🚪 **"Logout Now"** button for immediate logout

### **Activity Detection:**
- 🖱️ **Mouse movement** resets countdown
- ⌨️ **Keyboard input** resets countdown
- 🖱️ **Mouse clicks** reset countdown
- 📜 **Page scrolling** resets countdown

## 🌐 **Pages with Timeout Protection**

### **Protected Pages:**
- ✅ **Dashboard** (`/dashboard/`)
- ✅ **Time Logs** (`/time/logs/`)
- ✅ **All inventory pages**
- ✅ **CSV import/export pages**

### **Excluded Pages:**
- ❌ **Login page** (no timeout needed)
- ❌ **Home page** (public access)
- ❌ **Admin pages** (Django admin handles)

## 🚀 **Benefits**

### **For Management:**
- **Security compliance** with automatic session management
- **Prevents unauthorized access** to company data
- **Professional security** standards
- **Peace of mind** knowing sessions expire

### **For Employees:**
- **Clear warnings** before timeout
- **Easy to stay logged in** with activity
- **No accidental logouts** during active work
- **Automatic protection** when leaving computer

### **For Business:**
- **Enhanced security** for inventory system
- **Professional appearance** with modern timeout features
- **Compliance** with security best practices
- **User-friendly** timeout experience

---

## 🎉 **Session Timeout Feature Complete!**

The automatic session timeout feature is now fully functional with:
- ✅ **20-second timeout** for testing
- ✅ **Warning modal** 10 seconds before timeout
- ✅ **Activity detection** to prevent accidental timeouts
- ✅ **Server-side validation** for security
- ✅ **Easy configuration** for production use

**For production, simply change `SESSION_TIMEOUT = 600` in settings.py for 10-minute timeout!** 