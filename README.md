# Inventory Manager
A simple tool for tracking your inventory that runs directly from a USB flash drive on any Windows computer. No installation or internet connectivity required.

## Instructions
1. Download the recent release
2. Plug the flash drive into your Windows computer
3. Open the flash drive in **File Explorer**
4. Drag and drop **`InventoryManager.exe`** onto the flash drive
5. Double-click **`InventoryManager.exe`**

The program will open in a new window.

## First-Time Setup
Use the following default credentials to log in for the first time:

| Field | Value |
|---|---|
| **Username** | `Admin` |
| **Password** | `ChangeMe123!` |

Upon logging in, the system will automatically prompt you to create a **backup code** before accessing the program. This code is used to reset your password if you ever forget it.

**Creating your backup code:**
1. Log in with the default credentials above
2. A prompt will appear asking you to set a backup code
3. Enter a code that meets the following requirements:
   - At least 8 characters long
   - At least one uppercase letter
   - At least one lowercase letter
   - At least one number
   - At least one special character (e.g. `!@#$%`)
4. Click **OK** - you will be taken to the main inventory screen

> **Important:** Write your backup code down and store it somewhere safe. There is no way to recover it if lost. The only reset option is to delete the database (see Troubleshooting).

## Using the Program
| Feature | What it does |
|---|---|
| **Login** | Securely access your inventory with a username and password |
| **Add / Remove Items** | Add new inventory items or remove ones you no longer carry |
| **Manage Items** | Edit item details such as name, quantity, price, and notes |
| **Categories** | Organize items into categories to keep things tidy |
| **Sort Items** | Sort your inventory by name, quantity, price, or other fields |
| **Filter Items** | Narrow down your view to find specific items quickly |
| **To-Buy List** | Track items that are running low or need to be reordered |
| **Vendor Association** | Link items to their vendors for easy reference |

> Your data is saved directly to the flash drive. Nothing is stored online.

## Changing Your Password
If you need to change your password after logging in, use the **Forgot password?** link on the login screen.

1. Click **"Forgot password?"** on the login screen
2. Enter your **username** when prompted
3. Enter your **backup code** when prompted
4. Enter your **new password** when prompted

Your new password must meet the same requirements as the backup code listed in [First-Time Setup](#first-time-setup).

If successful, a confirmation message will appear, and you can log in with your new password immediately.

## Backing Up Your Data
To keep a backup of your inventory:
1. Plug in the flash drive
2. Copy the **entire flash drive data folder** to your computer or another safe location

## Something Not Working?

- **The `.exe` won't open**
Right-click `InventoryManager.exe` and select **"Run as Administrator"**, then try again.

- **A Windows security warning appeared**
Click **"More info"** then **"Run anyway"** - this is normal for programs not downloaded from an app store.

- **The program opens, but my data is missing**
Make sure the data folder is placed alongside the location of **`InventoryManager.exe`**.

- **My backup code is not being accepted when resetting my password**
Double-check that you are entering the backup code exactly as you set it - it is case-sensitive. If you are certain the code is correct and it still fails, see the reset step below.

- **I failed to set a backup code on the first login and cannot get past the prompt**
If you entered an invalid code and the setup failed, the program cannot proceed until a valid backup code is saved. To reset and start fresh:
1. Close the program
2. Navigate to **`docs/data/`** on the flash drive
3. Delete the file **`inventory.db`**
4. Relaunch **`InventoryManager.exe`** - the database will be recreated automatically and you can log in and set your backup code again

> **Note:** Deleting `inventory.db` will erase all saved inventory data. Only do this if you have no data worth keeping or have a backup copy saved elsewhere.
