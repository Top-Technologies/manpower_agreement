# Quick Start Guide - Manpower Distribution Tracking

## For New Users (Version 2.0+)

### Step 1: Verify Service Categories
1. Navigate to **Manpower Agreements > Configuration > Service Categories**
2. Review the 10 pre-configured categories
3. Add custom categories if needed (Managers only)

### Step 2: Create Your First Agreement
1. Go to **Manpower Agreements > Agreements**
2. Click **Create**
3. Fill in the basic information:
   - **Service Provider**: Select from manpower providers
   - **Receiving Business Unit**: Your company/branch
   - **Agreement Date**: Date of signing
   - **Effective Date**: When the agreement starts
   - **Expiration Date**: When it ends

### Step 3: Add Manpower Distribution
1. Click the **Manpower Distribution** tab
2. Click **Add a line**
3. For each service type you need:
   - Select **Service Category** (e.g., Security)
   - Enter **Male Workers** (e.g., 20)
   - Enter **Female Workers** (e.g., 5)
   - **Total** calculates automatically (25)
4. Add more lines for other categories (Cleaning, Drivers, etc.)
5. Review the **Summary** at the bottom:
   - Total Male Workers
   - Total Female Workers
   - Total Workers

### Step 4: Add Cost Details (Optional)
1. Click the **Cost and Payment** tab
2. Enter:
   - Service Fee
   - Manpower Rate per person
   - Rate Basis (per day/month/year)
   - Payment Frequency

### Step 5: Configure Renewal Settings
1. Click the **Renewal** tab
2. Set:
   - **Notify Before Expiry**: Days before expiry to get alert (default: 30)
   - **Responsible**: User who should receive notifications

### Step 6: Confirm the Agreement
1. Click **Confirm** button at the top
2. Agreement status changes to **Active**
3. Distribution is now locked (changes only via amendments)

## For Existing Users (Upgrading from 1.x)

### After Upgrade - First Steps

1. **Check Your Existing Agreements**
   - Open each agreement
   - You'll see the total manpower as 0 (this is expected)
   - The original quantity is stored but not displayed

2. **Add Distribution Lines to Existing Agreements**
   - For each agreement, go to **Manpower Distribution** tab
   - Add lines to represent the current workforce
   - If you don't know the category breakdown, use "Other" category
   - If you don't know gender breakdown, estimate or split 50/50

3. **Verify Totals Match**
   - After adding distribution lines, check the computed total
   - It should match your previous manpower quantity
   - If not, adjust the distribution lines

## Common Tasks

### View Provider's Total Manpower
1. Go to **Manpower Agreements > Service Providers**
2. Open a provider
3. See **Active Manpower Summary** showing:
   - Male, Female, and Total workers under active agreements
4. Click **Agreements** smart button to see all agreements

### Amend an Agreement (Change Quantities)
1. Open an **Active** agreement
2. Go to **Amendments** tab
3. Click **Add a line** or **Create**
4. Enter amendment details:
   - Date
   - Reason for change
5. Add amendment lines:
   - Select category
   - Enter new male and female quantities
   - Previous quantities shown for reference
6. Save
7. Agreement distribution updates automatically

### Renew an Expiring Agreement
1. Open the expiring agreement
2. Click **Renew** button
3. New agreement opens in Draft state with:
   - Same distribution as original
   - Start date = old end date + 1 day
4. Adjust dates and distribution as needed
5. Click **Confirm**

### Archive a Service Category
1. Go to **Configuration > Service Categories**
2. Open the category
3. Uncheck **Active**
4. Category archived (still usable in existing agreements)

**Note**: Don't delete categories that are in use - archive them instead!

## Tips and Best Practices

### Distribution Entry
- ✅ Add all relevant categories for accurate tracking
- ✅ Double-check male and female counts before confirming
- ✅ Use the Notes field to document special allocations
- ✅ Keep distribution updated via amendments

### Amendments
- ✅ Use amendments for all quantity changes after confirmation
- ✅ Document the reason for each amendment
- ✅ Review previous quantities before entering new ones
- ✅ Amendments create an audit trail in chatter

### Renewals
- ✅ Set appropriate notification days (30+ recommended)
- ✅ Assign responsible users to all agreements
- ✅ Check the "Expiring in 30 Days" filter weekly
- ✅ Review and update distribution when renewing

### Categories
- ✅ Use existing categories when possible
- ✅ Create custom categories only if needed
- ✅ Archive unused categories (don't delete)
- ✅ Use consistent naming conventions

## Troubleshooting

### "Total shows as 0 after upgrade"
**Cause**: No distribution lines added yet
**Solution**: Add distribution lines to match original quantity

### "Can't add duplicate category"
**Cause**: Category already exists on this agreement
**Solution**: Edit the existing line instead of adding a new one

### "Can't delete a category"
**Cause**: Category is used in distribution lines
**Solution**: Archive it instead (uncheck Active)

### "Can't edit distribution after confirmation"
**Cause**: Distribution locked when Active (by design)
**Solution**: Use amendments to change quantities

### "Provider summary doesn't match"
**Cause**: Only Active agreements are counted
**Solution**: Check agreement status (Draft/Expired/Terminated not included)

## Keyboard Shortcuts in Forms

- **Alt + C**: Confirm agreement (Draft → Active)
- **Alt + R**: Renew agreement
- **Alt + T**: Terminate agreement
- **Tab**: Move to next field
- **Ctrl + S**: Save (in edit mode)
- **Esc**: Cancel edit (in list)

## Report Filters

### Useful List View Filters
- **Active**: Shows only active agreements
- **Draft**: Shows only draft agreements
- **Expiring in 30 Days**: Critical for renewal planning
- **Expired**: Shows agreements that need action

### Grouping Options
- **By Provider**: See all agreements per provider
- **By Business Unit**: Organize by receiving unit
- **By Status**: Separate by lifecycle stage

## Getting Help

### In-App Help
- Hover over field labels for tooltips
- Check the info banner on Manpower Distribution tab
- Review chatter history for agreement changes

### Documentation
- **README.md**: Complete module documentation
- **UPGRADE_GUIDE.md**: Detailed upgrade instructions
- **IMPLEMENTATION_SUMMARY.md**: Technical details

### Support
Contact your Odoo administrator or implementation partner for:
- Custom category setup
- Bulk data migration
- Integration questions
- Training requests

---

## Quick Reference Card

| Task | Path | Button/Action |
|------|------|---------------|
| Create agreement | Agreements > Create | Fill form, add distribution, Confirm |
| View categories | Configuration > Service Categories | List view |
| Amend agreement | Open agreement > Amendments tab | Add a line |
| Renew agreement | Open agreement | Renew button |
| View provider summary | Service Providers > Open provider | See Active Manpower Summary |
| Check expiring | Agreements > Filter | "Expiring in 30 Days" |
| Add category line | Distribution tab | Add a line |
| View documents | Agreement form | Documents smart button |

---

**Version**: 2.0.0  
**Last Updated**: Implementation date  
**Module**: manpower_agreement
