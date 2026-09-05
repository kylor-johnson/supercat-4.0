# Product Requirements Document: User Invite Functionality

**Document Version:** 1.0  
**Date:** February 4, 2026  
**Author:** SuperCat Product Team  
**Status:** Draft for Review

---

## Executive Summary

Based on analysis of 183 user management support tickets from HelpScout (Hevo dataset), we've identified a significant opportunity to improve the user onboarding experience through self-service invite functionality. Currently, **26.8% of all user management tickets** are related to adding new users, inviting reps, or requesting credentials.

### Key Findings

- **183 total user management tickets** analyzed (2025-2026)
- **49 tickets (26.8%)** specifically related to new user/invite workflows
- **75.5%** of invite-related requests are for credentials/login info
- **Average resolution time:** 42.5 hours (1.8 days)
- **25% of tickets** could be handled through self-service functionality
- **High-touch customers:** Capital Lighting (18 tickets), Wildwood (8 tickets), Charleston Forge (7 tickets)

### Business Impact

Implementing self-service user invite functionality could:
- **Reduce support burden** by ~25% for user management tickets
- **Improve time-to-value** for new users from 1.8 days to <1 hour
- **Increase customer satisfaction** by enabling immediate user onboarding
- **Scale user operations** without proportional support team growth

---

## Problem Statement

### Current State Pain Points

1. **Manual Support Dependency**
   - Admins must contact support to add new users
   - Average 1.8 day wait time for new user setup
   - 33.3% of tickets encounter errors or issues

2. **Credential Management Friction**
   - 75.5% of requests are for username/password delivery
   - No automated welcome email with login instructions
   - Password reset issues create additional support tickets

3. **High-Touch Complexity**
   - 25% of tickets require >6 support interactions
   - Slowest resolution: 7 days for a simple username change
   - Configuration errors require back-and-forth with support

4. **Scalability Limitations**
   - No bulk user import capability
   - High-volume customers create repetitive support requests
   - Each new employee requires manual support intervention

### User Personas Affected

**Primary Persona: Company Administrator**
- Needs to onboard new sales reps quickly
- Wants to manage user access independently
- Frustrated by delays in getting new employees productive

**Secondary Persona: New User/Rep**
- Waiting for credentials to access the platform
- Unclear onboarding process
- May need multiple password resets

---

## Solution Overview

### Vision

Enable company administrators to independently invite, manage, and onboard new users through an intuitive self-service interface, reducing time-to-productivity from days to minutes.

### Core Capabilities

1. **Self-Service User Invites**
2. **Automated Credential Delivery**
3. **Bulk User Import**
4. **User Management Dashboard**
5. **Role-Based Quick Setup**

---

## Detailed Requirements

### 1. Self-Service User Invites

**Priority:** P0 (Must Have)  
**Estimated Impact:** Reduce 25% of user management tickets

#### Functional Requirements

**FR-1.1: Invite User Interface**
- Admin can access "Invite User" button from user management page
- Form includes:
  - Email address (required, validated)
  - First name (required)
  - Last name (required)
  - Role selection (required): Rep, Manager, Admin
  - Optional: Phone number, Territory assignment
- Real-time email validation
- Clear error messaging for invalid inputs

**FR-1.2: Invite Email Delivery**
- System sends automated invite email immediately upon submission
- Email includes:
  - Personalized welcome message
  - Company name and logo
  - Secure invite link (expires in 7 days)
  - Instructions for first-time login
  - Link to getting started guide/video
  - Support contact information
- Email template customizable by company admin
- Sent from branded @supercat.com address

**FR-1.3: Invite Link Security**
- Unique, single-use invite token
- 7-day expiration (configurable)
- HTTPS only
- Token invalidated after first use
- Expired invites can be resent

**FR-1.4: Password Setup Flow**
- New user clicks invite link
- Redirected to password creation page
- Password requirements displayed:
  - Minimum 8 characters
  - At least 1 uppercase letter
  - At least 1 number
  - At least 1 special character
- Password strength indicator
- Confirm password field
- Upon completion, user is logged in automatically

**FR-1.5: Invite Status Tracking**
- Admin can view invite status: Pending, Accepted, Expired
- Last sent timestamp
- Option to resend invite
- Option to cancel pending invite
- Email notification to admin when invite is accepted

#### Non-Functional Requirements

**NFR-1.1: Performance**
- Invite email sent within 30 seconds of submission
- Page load time <2 seconds
- Support 100 concurrent invite operations

**NFR-1.2: Reliability**
- 99.9% email delivery success rate
- Retry logic for failed email sends
- Logging of all invite operations for audit

**NFR-1.3: Security**
- Invite tokens use cryptographically secure random generation
- Rate limiting: Max 50 invites per admin per hour
- Email verification required for new admin accounts
- Audit log of all invite activities

#### Success Metrics

- 80% of new users complete setup within 24 hours
- 50% reduction in "new user" support tickets
- <5% invite email bounce rate
- 90% admin satisfaction score

---

### 2. Automated Credential Delivery

**Priority:** P0 (Must Have)  
**Estimated Impact:** Eliminate 75.5% of credential request tickets

#### Functional Requirements

**FR-2.1: Welcome Email**
- Automatically sent upon invite acceptance
- Includes:
  - Username (auto-generated or email-based)
  - Link to reset/set password
  - Direct login link
  - Getting started checklist
  - Video tutorial links
  - FAQ section

**FR-2.2: Username Generation**
- Option 1: Use email address as username
- Option 2: Auto-generate from first.last name
- Option 3: Allow user to choose during setup
- Check for uniqueness across organization
- Display username clearly in welcome email

**FR-2.3: Password Reset Integration**
- Include password reset link in welcome email
- Self-service password reset flow
- Security questions or email verification
- No support intervention required

#### Success Metrics

- 90% reduction in "credentials request" tickets
- <1% password reset failures
- 95% of users successfully log in on first attempt

---

### 3. Bulk User Import

**Priority:** P1 (Should Have)  
**Estimated Impact:** Reduce high-touch tickets by 25%

#### Functional Requirements

**FR-3.1: CSV Upload Interface**
- "Import Users" button on user management page
- Download CSV template with required columns:
  - Email (required)
  - First Name (required)
  - Last Name (required)
  - Role (required)
  - Phone (optional)
  - Territory (optional)
- Drag-and-drop file upload
- Maximum 500 users per upload

**FR-3.2: Validation & Preview**
- Real-time validation of CSV format
- Preview of users to be imported
- Highlight errors/warnings:
  - Invalid email format
  - Duplicate emails
  - Missing required fields
  - Invalid role values
- Show count: X valid, Y errors
- Allow correction before import

**FR-3.3: Batch Processing**
- Process imports asynchronously
- Progress indicator
- Email notification when complete
- Summary report:
  - Successfully imported: X users
  - Failed: Y users (with reasons)
  - Invites sent: Z emails
- Download error report for failed imports

**FR-3.4: Bulk Invite Sending**
- Option to send invites immediately or schedule
- Throttle email sending to avoid spam filters
- Track bulk invite status in dashboard

#### Success Metrics

- 80% of high-volume customers adopt bulk import
- <5% error rate on bulk imports
- 70% reduction in repetitive "add user" tickets from same customers

---

### 4. User Management Dashboard

**Priority:** P1 (Should Have)  
**Estimated Impact:** Improve admin efficiency by 50%

#### Functional Requirements

**FR-4.1: User List View**
- Searchable, sortable table of all users
- Columns:
  - Name
  - Email
  - Role
  - Status (Active, Pending Invite, Inactive)
  - Last Login
  - Actions (Edit, Deactivate, Resend Invite)
- Filters:
  - By role
  - By status
  - By territory
- Pagination (50 users per page)

**FR-4.2: User Actions**
- Quick actions from list view:
  - Resend invite (for pending users)
  - Deactivate user (with confirmation)
  - Edit user details
  - Reset password
  - Change role
- Bulk actions:
  - Select multiple users
  - Bulk deactivate
  - Bulk role change
  - Export to CSV

**FR-4.3: User Detail View**
- Click user to view full profile
- Display:
  - Contact information
  - Role and permissions
  - Account creation date
  - Last login date
  - Activity history
  - Assigned territories/accounts
- Edit button to modify details
- Activity log of admin changes

**FR-4.4: Pending Invites Section**
- Dedicated section for pending invites
- Show:
  - Invited user email
  - Invited by (admin name)
  - Sent date
  - Expiration date
  - Status
- Actions:
  - Resend invite
  - Cancel invite
  - Copy invite link

#### Success Metrics

- 90% of admins use dashboard weekly
- 60% reduction in "user status" inquiries
- <3 clicks to complete common tasks

---

### 5. Role-Based Quick Setup

**Priority:** P2 (Nice to Have)  
**Estimated Impact:** Reduce resolution time by 77.8%

#### Functional Requirements

**FR-5.1: Role Templates**
- Pre-configured permission sets:
  - **Rep Role:**
    - View products
    - Create orders
    - View own customers
    - No admin access
  - **Manager Role:**
    - All Rep permissions
    - View team performance
    - Approve orders
    - Manage territory assignments
  - **Admin Role:**
    - All Manager permissions
    - User management
    - Company settings
    - Billing access

**FR-5.2: Role Selection During Invite**
- Dropdown menu with role options
- Tooltip explaining each role's permissions
- Preview of permissions before sending invite
- Option to customize permissions (advanced)

**FR-5.3: Custom Roles**
- Admin can create custom roles
- Copy existing role as template
- Granular permission toggles
- Save custom role for future use
- Assign custom role during invite

**FR-5.4: Role Change**
- Change user role from dashboard
- Confirmation dialog showing permission changes
- Email notification to user about role change
- Audit log of role changes

#### Success Metrics

- 85% of invites use standard role templates
- <10% require custom permission configuration
- 50% reduction in permission-related support tickets

---

## User Experience Flow

### Happy Path: Admin Invites New Rep

1. **Admin logs into platform**
2. **Navigates to User Management**
3. **Clicks "Invite User" button**
4. **Fills out invite form:**
   - Email: newrep@company.com
   - Name: John Doe
   - Role: Rep
5. **Clicks "Send Invite"**
6. **System validates and sends email**
7. **Admin sees confirmation: "Invite sent to newrep@company.com"**
8. **New user receives email within 30 seconds**
9. **User clicks invite link**
10. **User sets password**
11. **User is logged in and sees onboarding checklist**
12. **Admin receives notification: "John Doe accepted invite"**

**Total Time:** <5 minutes (vs. 1.8 days currently)

### Edge Cases

**EC-1: Email Bounce**
- System detects bounce
- Admin receives notification
- Admin can update email and resend

**EC-2: Expired Invite**
- User clicks expired link
- Sees friendly error message
- Option to request new invite
- Admin receives notification to resend

**EC-3: Duplicate Email**
- System detects existing user
- Shows error: "User already exists"
- Option to resend invite or view existing user

**EC-4: User Doesn't Receive Email**
- Admin can check invite status
- See "Sent" timestamp
- Option to resend
- Copy invite link to send manually

---

## Technical Considerations

### Architecture

**Frontend:**
- React components for invite forms and dashboard
- Real-time validation using Formik/Yup
- Toast notifications for success/error states

**Backend:**
- RESTful API endpoints:
  - POST /api/users/invite
  - GET /api/users/invites
  - POST /api/users/invites/:id/resend
  - DELETE /api/users/invites/:id
  - POST /api/users/bulk-import
- Background job queue for email sending
- Token generation and validation service

**Database:**
- User invites table:
  - id, email, token, status, expires_at, invited_by, created_at
- User roles table:
  - id, name, permissions (JSON)
- Audit log table:
  - id, user_id, action, timestamp, details

**Email Service:**
- Integration with SendGrid/AWS SES
- Template management system
- Bounce/complaint handling
- Delivery tracking

### Security

- OWASP Top 10 compliance
- Rate limiting on invite endpoints
- CAPTCHA for public-facing invite acceptance
- Encryption of invite tokens at rest
- Audit logging of all user management actions
- GDPR compliance for user data

### Scalability

- Horizontal scaling of API servers
- Redis cache for invite token validation
- Async job processing for bulk operations
- CDN for static assets
- Database read replicas for reporting

---

## Implementation Phases

### Phase 1: MVP (4-6 weeks)
- Self-service single user invite
- Automated welcome email
- Basic user dashboard
- Standard role templates

**Success Criteria:**
- 50% reduction in new user support tickets
- 90% invite acceptance rate
- <2 second page load time

### Phase 2: Bulk Operations (2-3 weeks)
- CSV bulk import
- Batch invite sending
- Enhanced dashboard with filters
- Invite status tracking

**Success Criteria:**
- 5+ customers using bulk import
- <5% error rate on imports
- 70% reduction in high-volume customer tickets

### Phase 3: Advanced Features (3-4 weeks)
- Custom role creation
- Advanced permission management
- Onboarding workflow builder
- Integration with SSO providers

**Success Criteria:**
- 30% of customers using custom roles
- SSO adoption by enterprise customers
- 95% admin satisfaction score

---

## Success Metrics & KPIs

### Primary Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Avg. time to new user activation | 42.5 hours | <1 hour | Time from invite to first login |
| User management support tickets | 183/year | <100/year | HelpScout ticket count |
| Invite acceptance rate | N/A | >90% | Accepted invites / Total sent |
| Admin satisfaction | N/A | >90% | NPS survey |

### Secondary Metrics

- Email delivery success rate: >99%
- Password reset success rate: >95%
- Bulk import adoption: >50% of high-volume customers
- Dashboard usage: >80% of admins weekly
- Self-service resolution: >75% of invite workflows

---

## Risks & Mitigations

### Risk 1: Email Deliverability
**Impact:** High  
**Likelihood:** Medium  
**Mitigation:**
- Use reputable email service (SendGrid/AWS SES)
- Implement DKIM, SPF, DMARC
- Monitor bounce rates
- Provide alternative invite link copy option

### Risk 2: Security Vulnerabilities
**Impact:** Critical  
**Likelihood:** Low  
**Mitigation:**
- Security audit before launch
- Penetration testing
- Rate limiting and CAPTCHA
- Regular security updates

### Risk 3: User Adoption
**Impact:** High  
**Likelihood:** Low  
**Mitigation:**
- In-app tutorials and tooltips
- Email announcement to all admins
- Support team training
- Gradual rollout with beta customers

### Risk 4: Performance Issues
**Impact:** Medium  
**Likelihood:** Low  
**Mitigation:**
- Load testing before launch
- Async processing for bulk operations
- Caching strategy
- Monitoring and alerting

---

## Open Questions

1. **Should we support SSO integration in Phase 1?**
   - Recommendation: Phase 3 to avoid complexity
   
2. **What should the default invite expiration be?**
   - Recommendation: 7 days (industry standard)
   
3. **Should admins be able to set custom email templates?**
   - Recommendation: Phase 2 feature
   
4. **How do we handle users with multiple roles across organizations?**
   - Recommendation: Separate user profiles per organization
   
5. **Should we allow users to self-register or require invite?**
   - Recommendation: Invite-only for security and control

---

## Appendix

### A. Support Ticket Analysis Summary

**Data Source:** BigQuery (hevo_dataset_supercat_data_pipeline_Slhk.help_scout_tickets)  
**Date Range:** January 2025 - February 2026  
**Total Tickets Analyzed:** 183 user management tickets

**Key Findings:**
- 56.8% "Other User Management" (general admin tasks)
- 19.7% Credentials Request
- 9.3% Password Reset
- 4.9% Access/Permission Issues
- 3.8% New User Account Setup
- 3.3% Add/Invite User

**Top Pain Points:**
- 33.3% encountering errors/issues
- 33.3% password/credential issues
- 75.5% requesting credentials/login info

**Resolution Time:**
- Average: 42.5 hours
- Median: 23.0 hours
- 22.2% resolved in <2 hours
- 22.2% took >48 hours

**Complexity:**
- 33.3% single-touch (1 thread)
- 33.3% medium-touch (4-6 threads)
- 25.0% high-touch (>6 threads)

### B. Customer Feedback Quotes

> "We have a new sales rep starting Monday and need to get them set up ASAP. Can you create their account today?" - Capital Lighting

> "I've been waiting 3 days for the username and password for our new employee. Is there a way we can do this ourselves?" - Wildwood

> "We're onboarding 5 new reps next month. Is there a bulk import option?" - Charleston Forge

> "The new user didn't receive the welcome email. Can you resend it?" - Minka Group

### C. Competitive Analysis

**Competitor A (Salesforce):**
- Self-service user invite ✅
- Role-based templates ✅
- Bulk import ✅
- SSO integration ✅

**Competitor B (HubSpot):**
- Self-service user invite ✅
- Simple role selection ✅
- Limited bulk operations ⚠️
- Email automation ✅

**SuperCat (Current):**
- Self-service user invite ❌
- Manual support required ❌
- No bulk operations ❌
- No automated emails ❌

**Opportunity:** Implementing these features brings SuperCat to competitive parity and improves customer experience significantly.

---

## Approval & Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | | | |
| Engineering Lead | | | |
| Design Lead | | | |
| Support Manager | | | |
| Security Lead | | | |

---

**Document History:**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-04 | SuperCat Product Team | Initial draft based on support ticket analysis |
