select first_choice,count(first_choice) AS Co FROM dtlms_recruitment_applications WHERE 
application_status = ('initial_screening_first') 
AND (candidate_no IS NOT NULL OR candidate_no!='') 
AND first_choice_screening_submitted_at IS NULL
group by first_choice ORDER BY co DESC;