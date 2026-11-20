# Manpower Agreement Module - Version 2.0.0 Upgrade Guide

## Overview

Version 2.0.0 introduces **Manpower Distribution by Service Category and Gender**, a major enhancement that allows detailed tracking of workforce allocation across different service categories with gender breakdown.

## What's New

### 1. Service Categories
- New configurable service category model (`manpower.service.category`)
- Pre-configured categories: Security, Cleaning, Housekeeping, Gardening, Loading & Unloading, Drivers, Technical Maintenance, Production Support, Office Support, and Other
- Managers can create, edit, and archive categories via **Configuration > Service Categories**

### 2. Distribution Lines
- Each agreement can now track manpower by service category and gender
- New **Manpower Distribution** tab on agreement form
- Separate counts for Male and Female workers per category
- Automatic calculation of totals

### 3. Enhanced Agreement Model
- `manpower_qty` is now **computed** from distribution lines (was manual entry)
- New fields: `male_qty`, `female_qty`, `manpower_distribution_ids`
- Agreement totals automatically update when distribution lines change

### 4. Provider-Level Summaries
- Providers now show aggregate manpower from active agreements
- New fields on `res.partner`: `active_male_qty`, `active_female_qty`, `active_manpower_qty`
- Visible on the Service Provider form

### 5. Enhanced Amendments
- Amendments now work with distribution lines
- New `manpower.agreement.amendment.line` model
- Amendment form shows category-by-category changes
- Approved amendments update agreement distribution automatically

## Installation and Upgrade

### Fresh Installation
1. Install the module normally through Odoo Apps
2. Service categories will be created automatically
3. No additional configuration needed

### Upgrading from Version 1.x

#### Important: Data Migration Considerations

**The `manpower_qty` field is now computed from distribution lines.** Existing agreements with a manually-entered `manpower_qty` will retain this value in the database, but:

1. **If distribution lines exist**, the computed total will override the legacy value
2. **If no distribution lines exist**, the legacy `manpower_qty` will appear as zero in the UI

#### Migration Options

**Option A: Manual Migration (Recommended for small datasets)**
1. Upgrade the module
2. Review each existing agreement
3. Add distribution lines to match the original `manpower_qty`
4. Since there's no historical gender/category data, use your best judgment or assign all workers to "Other" category

**Option B: Preserve Legacy Totals (Contact developers)**
If you have many agreements and need an automated migration that preserves legacy quantities, a custom migration script can be developed to:
- Create a distribution line in the "Other" category for each existing agreement
- Split quantities proportionally if gender data is available elsewhere
- This would require custom development outside the scope of this enhancement

#### Safe Upgrade Steps

1. **Backup your database** before upgrading
2. Update the module code to version 2.0.0
3. Upgrade the module in Odoo (Apps > Manpower Supply Agreement Management > Upgrade)
4. Test in a staging environment first
5. Review existing agreements and add distribution lines as needed
6. Train users on the new distribution tracking workflow

## Breaking Changes

### Field Changes
- `manpower_qty` on `manpower.agreement`: Changed from **editable** to **computed** (store=True)
- Removed write override that blocked `manpower_qty` changes after draft state
- `manpower_qty` is now derived from distribution lines only

### Amendment Model Changes
- `new_qty` on `manpower.agreement.amendment`: Changed to **computed** from amendment lines
- Amendments no longer directly write `manpower_qty`
- Amendments now update distribution lines, which triggers recomputation

### View Changes
- "Manpower Quantity" tab renamed to "Manpower Distribution"
- Distribution line grid added to agreement form
- Amendments moved to separate tab

## User Workflow Changes

### Creating a New Agreement (Version 2.0+)
1. Create agreement in Draft state
2. Go to **Manpower Distribution** tab
3. Add lines for each service category needed
4. Enter male and female quantities for each category
5. View computed totals at bottom of the page
6. Confirm agreement

### Amending an Existing Agreement
1. Open an Active agreement
2. Go to **Amendments** tab
3. Create a new amendment
4. Add amendment lines showing new quantities per category
5. Save the amendment
6. Agreement distribution will update automatically

### Viewing Provider Summaries
1. Go to **Manpower Agreements > Service Providers**
2. Open a provider
3. View **Active Manpower Summary** section showing:
   - Total Male Workers
   - Total Female Workers
   - Total Workers
4. These totals reflect only Active agreements

## Security

### Access Rights
- **Manpower Users**: Can read service categories; can create/edit distribution lines on Draft agreements
- **Manpower Managers**: Full access to service categories and distribution lines; can manage amendments

### New Access Control Entries
- `manpower.service.category` (Users: read; Managers: all)
- `manpower.agreement.line` (Users: create/read/write; Managers: all)
- `manpower.agreement.amendment.line` (Users: read; Managers: all)

## Technical Notes

### Computed Field Dependencies
```python
@api.depends('manpower_distribution_ids.male_qty',
             'manpower_distribution_ids.female_qty',
             'manpower_distribution_ids.total_qty')
def _compute_manpower_totals(self):
    # Computes male_qty, female_qty, manpower_qty
```

### Constraints
- Distribution line quantities must be non-negative
- No duplicate categories per agreement (SQL constraint)
- Category codes must be unique if provided
- Categories used in distribution lines cannot be deleted (must archive)

### Agreement Renewal
- Distribution lines are copied to renewed agreements (copy=True)
- Totals recompute automatically on the new agreement
- Previous agreement linkage preserved

## Configuration Menu

A new **Configuration** menu has been added (Managers only):
- **Configuration > Service Categories**: Manage service category master data

## API Changes

### New Models
- `manpower.service.category`
- `manpower.agreement.line`
- `manpower.agreement.amendment.line`

### New Fields on `manpower.agreement`
- `manpower_distribution_ids` (One2many)
- `male_qty` (Integer, computed, stored)
- `female_qty` (Integer, computed, stored)

### New Fields on `res.partner`
- `active_male_qty` (Integer, computed)
- `active_female_qty` (Integer, computed)
- `active_manpower_qty` (Integer, computed)

### Modified Fields on `manpower.agreement.amendment`
- `new_qty`: Now computed from `amendment_line_ids`
- New One2many: `amendment_line_ids`

## Support and Questions

For technical support or questions about this upgrade:
1. Review this guide thoroughly
2. Test in a non-production environment
3. Contact your Odoo implementation partner if custom migration is needed

## Version History

- **2.0.0** (Current): Added service category and gender-based distribution tracking
- **1.0.2**: Original release with basic agreement management

---

**Recommendation**: Perform this upgrade during a planned maintenance window and ensure all users are trained on the new distribution tracking workflow before go-live.
