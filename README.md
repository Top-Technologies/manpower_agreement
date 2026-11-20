# Manpower Supply Agreement Management

## Overview

This Odoo 18 module provides comprehensive management of manpower supply agreements with external service providers. Track workforce distribution by service category and gender, manage contract terms, handle amendments, and monitor agreement lifecycles.

## Key Features

### 1. Agreement Management
- **Complete Agreement Lifecycle**: Draft → Active → Expired/Terminated
- **Automated Sequence**: Unique agreement reference numbers
- **Multi-Company Support**: Business unit assignment
- **Contract Terms**: Store detailed contractual terms and conditions
- **Document Integration**: Attach and manage related documents
- **Chatter Integration**: Full activity tracking and messaging

### 2. Manpower Distribution Tracking
- **Service Category Classification**: Track workers by type of service
- **Gender Breakdown**: Separate male and female worker counts
- **Automatic Totals**: Computed agreement-level summaries
- **Flexible Categories**: Configurable service category master data

**Pre-configured Service Categories:**
- Security
- Cleaning
- Housekeeping
- Gardening
- Loading & Unloading
- Drivers
- Technical Maintenance
- Production Support
- Office Support
- Other

### 3. Provider Management
- **Provider Directory**: Dedicated service provider database
- **Agreement History**: Track all agreements per provider
- **Active Manpower Summary**: Aggregate view of current workforce
- **Provider Classification**: Flag and manage manpower providers

### 4. Cost and Payment Terms
- **Service Fees**: Track agreement-level service charges
- **Manpower Rates**: Per-person or lump-sum pricing
- **Rate Basis**: Per day, month, year, or lump sum
- **Payment Frequency**: Weekly, monthly, quarterly, semi-annual, or annual
- **Other Charges**: Additional contractual costs
- **Payment Terms**: Detailed payment condition documentation

### 5. Amendments
- **Formal Amendment Process**: Track quantity changes
- **Distribution-Level Amendments**: Modify category/gender allocations
- **Amendment History**: Complete audit trail
- **Approval Tracking**: Record who approved each amendment
- **Automatic Agreement Updates**: Amendments update distribution automatically

### 6. Renewal Management
- **Expiry Notifications**: Automated alerts before agreement expires
- **Configurable Notice Period**: Set notification days per agreement
- **One-Click Renewal**: Create new agreement from expiring one
- **Renewal Linkage**: Track agreement renewal chain
- **Smart Status Indicators**: Visual warning for expiring agreements

### 7. Automated Workflows
- **Daily Cron Job**: Checks for expiring and expired agreements
- **Activity Scheduling**: Assigns renewal tasks to responsible users
- **Automatic State Transitions**: Moves Active → Expired on expiry date
- **Email Notifications**: Alerts via chatter for upcoming expirations

## Installation

### Requirements
- Odoo 18.0
- Base modules: `base`, `mail`, `documents`

### Install Steps
1. Copy the `manpower_agreement` folder to your Odoo addons directory
2. Update the apps list: **Settings > Apps > Update Apps List**
3. Search for "Manpower Supply Agreement Management"
4. Click **Install**

Service categories will be created automatically during installation.

## Configuration

### 1. User Access Rights

Navigate to **Settings > Users & Companies > Groups**

**Manpower User**
- View and create agreements
- Manage draft agreements
- View service providers
- View service categories

**Manpower Manager** (includes User rights plus)
- Delete agreements
- Manage service categories
- Full amendment control
- Access to all configuration

### 2. Service Categories

**Path**: Manpower Agreements > Configuration > Service Categories

- View and manage service category master data
- Create custom categories beyond the defaults
- Archive unused categories (don't delete if used in agreements)
- Set sequence for ordering

### 3. Agreement Notification

Each agreement has:
- **Responsible User**: Who receives expiry notifications
- **Notice Days**: How many days before expiry to send alerts

## Usage

### Creating an Agreement

1. Navigate to **Manpower Agreements > Agreements**
2. Click **Create**
3. Fill in basic information:
   - Service Provider (must be flagged as manpower provider)
   - Receiving Business Unit
   - Agreement Date, Effective Date, Expiration Date
4. Go to **Manpower Distribution** tab
5. Add distribution lines:
   - Select Service Category
   - Enter Male Workers count
   - Enter Female Workers count
   - Total calculates automatically
6. Review computed totals at bottom
7. Optional: Fill in **Cost and Payment** details
8. Optional: Set **Renewal** parameters
9. Click **Confirm** to activate

### Managing Distribution

**Adding a Category:**
1. In the Manpower Distribution tab, click **Add a line**
2. Select Category from dropdown
3. Enter Male and Female quantities
4. Total updates automatically

**Editing Quantities:**
1. Click on a line to edit
2. Modify male or female quantities
3. Agreement totals recompute automatically

**Removing a Category:**
1. Click the trash icon on the line
2. Agreement totals update immediately

### Creating an Amendment

1. Open an **Active** agreement
2. Go to **Amendments** tab
3. Click **Add a line** or **Create**
4. Fill in:
   - Date
   - Reason for amendment
5. Add amendment lines:
   - Select Category
   - Enter new Male and Female quantities
   - Previous quantities shown for reference
6. Save
7. Agreement distribution updates automatically
8. Amendment posted to chatter

### Renewing an Agreement

1. Open an agreement nearing expiry
2. Click **Renew** button
3. New agreement created in Draft state with:
   - Same provider and business unit
   - Start date = old expiry date + 1 day
   - End date = old expiry date + 366 days
   - Same distribution lines (editable)
4. Review and adjust as needed
5. Click **Confirm**

### Viewing Provider Summaries

1. Navigate to **Manpower Agreements > Service Providers**
2. Open a provider
3. View **Active Manpower Summary** showing:
   - Total Male Workers under active agreements
   - Total Female Workers under active agreements
   - Total Workers
4. Click **Agreements** smart button to see all agreements

## Reports and Analysis

### List Views

**Agreement List** shows:
- Agreement Reference
- Provider
- Business Unit
- Start and End Dates
- Male, Female, and Total Workers
- Payment Frequency
- Status

**Grouping Options:**
- By Provider
- By Business Unit
- By Status

**Filters:**
- Active Agreements
- Draft Agreements
- Expiring in 30 Days
- Expired Agreements

### Provider View

Service provider form displays aggregated active manpower totals, providing instant visibility into current workforce supply.

## Technical Information

### Models

**manpower.agreement**
- Main agreement model with lifecycle management
- Computed fields for male, female, and total quantities
- Integration with mail.thread and mail.activity.mixin

**manpower.service.category**
- Service category master data
- Prevents deletion of used categories

**manpower.agreement.line**
- Distribution lines linking agreement to categories
- Male/female quantity tracking
- Computed total per line
- SQL constraint prevents duplicate categories per agreement

**manpower.agreement.amendment**
- Amendment header with date and reason
- Computed new_qty from amendment lines
- Automatically updates agreement distribution

**manpower.agreement.amendment.line**
- Category-level amendment details
- Tracks previous and new quantities
- Applies changes to agreement distribution

**res.partner** (extended)
- is_manpower_provider flag
- Computed active manpower summaries
- Agreement count and smart button

### Key Constraints

- Agreement end date must be after start date
- Distribution quantities must be non-negative
- Category codes must be unique
- No duplicate categories per agreement
- Categories in use cannot be deleted (must archive)

### Automated Jobs

**Cron: Check Manpower Agreement Expiry**
- Runs daily
- Sends notifications for agreements approaching expiry
- Automatically transitions Active → Expired on expiry date
- Creates activities for responsible users

## Multi-Company Considerations

- Each agreement assigned to one business unit (company)
- Provider summaries aggregate across all agreements
- Ensure proper record rules if strict company isolation needed
- Service categories shared across all companies

## Upgrade Notes

See [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md) for detailed information on upgrading from version 1.x to 2.x.

**Key Change in Version 2.0:**
- `manpower_qty` is now computed from distribution lines
- Legacy agreements may require manual distribution entry
- Backup before upgrading

## Best Practices

1. **Always test in staging** before upgrading production
2. **Set responsible users** on all agreements for proper notifications
3. **Archive unused categories** rather than deleting
4. **Use amendments** for formal quantity changes on active agreements
5. **Review expiring agreements** weekly using the "Expiring in 30 Days" filter
6. **Attach documents** to agreements for contract scan, invoices, etc.
7. **Use chatter** to log important agreement-related communications

## Support

For questions or issues:
1. Review this README and the UPGRADE_GUIDE
2. Check the module's inline help text
3. Contact your Odoo implementation partner

## License

LGPL-3

## Credits

**Author**: Custom Development
**Version**: 2.0.0
**Odoo Version**: 18.0
