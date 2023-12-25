In a team of 4 build a ATS Job System that helps job seeker to find jobs based on it's resume with better search result and with a better chance to get a job.

Prototype Images:
1. Sign Up: User data is stored in RDS.
   
   ![Sign Up](https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/fd8349aa-cf6f-4212-9088-996e8fb33d4e)

   RDS:
   
   <img width="1440" alt="RDS Instance" src="https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/72f18bcf-2f9b-4827-9b16-d6643d25acf0">

   <img width="1018" alt="PostgreSQL RDS data stored" src="https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/10672625-d5a7-418b-b195-6499d455bffa">

3. Login:
   
   ![Login](https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/53bc3917-b527-45e9-9e7c-19691247fa8a)

4. Add Required Job Details: Resume and job details are stored in S3 Bucket
   
   ![Add Job Details](https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/b930707f-90e7-4758-b970-87043fdf14dc)

   S3 Bucket:

   <img width="723" alt="S3 Buckets" src="https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/c22a3ab4-71f1-4ab0-bbbd-19b68b682cf1">

   <img width="1440" alt="S3 Bucket Object Resume" src="https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/3cd02b05-95a3-45a1-8508-14b9a67dcc8f">

5. Job Listings: Jobs are fetched based on resume and job details from Adzuna and sorted & showed based on resume score using matching words.
   
   ![Job Listings](https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/4d307d9f-5f85-4236-91e1-752b52855261)

6. Apply: Each job showcase resume score and missing skills as follows.
    
   ![Apply API](https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/823713b9-b006-42dc-a10f-9e4b8703d608)

7. Deployment: EC2

   ![EC2](https://github.com/ronakkkk/ATS-Get-Job/assets/37010825/42351b3b-506a-4835-9c41-839e237ae297)





