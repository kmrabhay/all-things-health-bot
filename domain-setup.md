# Setting up Custom Domain for Healthy Nation

To connect your domain `healthynation.in` to your CloudFront distribution, follow these steps:

## Step 1: Update your DNS settings

Log in to your domain registrar (where you purchased `healthynation.in`) and add the following DNS records:

### Option 1: Using a CNAME record (recommended for subdomains)

Add a CNAME record:
- **Name/Host**: `www` (or @ for root domain if your registrar supports CNAME at root)
- **Value/Target**: `d1c7f7ldk0qchl.cloudfront.net`
- **TTL**: 3600 (or as low as possible)

### Option 2: Using an A record with ALIAS (for root domain)

If your DNS provider supports ALIAS records (like Route 53):
- **Record Type**: A
- **Name/Host**: @ (or leave blank for root domain)
- **Value/Target**: `d1c7f7ldk0qchl.cloudfront.net`
- **TTL**: 3600 (or as low as possible)

## Step 2: Set up SSL Certificate

Since you're not using Route 53, you'll need to manually set up an SSL certificate:

1. Go to AWS Certificate Manager (ACM) in the **us-east-1** region (important!)
2. Request a public certificate for `healthynation.in` and `www.healthynation.in`
3. Choose DNS validation
4. Add the validation CNAME records to your DNS settings at your registrar
5. Wait for the certificate to be issued (can take up to 30 minutes)

## Step 3: Update CloudFront Distribution

1. Go to CloudFront in the AWS Console
2. Select your distribution (`d1c7f7ldk0qchl.cloudfront.net`)
3. Click "Edit"
4. Under "Alternate Domain Names (CNAMEs)", add:
   - `healthynation.in`
   - `www.healthynation.in`
5. Under "Custom SSL Certificate", select the certificate you created
6. Save changes

## Step 4: Wait for DNS Propagation

DNS changes can take 24-48 hours to fully propagate, though often they work much sooner.

## Testing Your Setup

After DNS propagation, your site should be accessible at:
- https://healthynation.in
- https://www.healthynation.in

## Troubleshooting

If your site doesn't work after 48 hours:

1. Verify DNS records are correct using a tool like [DNSChecker](https://dnschecker.org)
2. Ensure the CloudFront distribution is properly configured with your domain names
3. Check that the SSL certificate is valid and properly associated with the distribution
4. Try clearing your browser cache or testing from a different network