delete from trt_patient  where fullname = '刘梅';
delete from trt_patient_common  where fullname = '刘梅';
delete from trt_patient_handle  where p_id in (select id from trt_patient  where fullname = '刘梅');
delete from trt_patient_record  where pid in (select id from trt_patient  where fullname = '刘梅');
delete from trt_patient_score  where p_id in (select id from trt_patient  where fullname = '刘梅');
delete from trt_patient_sign  where p_id in (select id from trt_patient  where fullname = '刘梅');
delete from trt_patient_symptom  where patient_id in (select id from trt_patient  where fullname = '刘梅');
delete from trt_special_patient  where cardnum in ('698515201409041111');
delete from trt_calling_patient  where patient_id in (select id from trt_patient  where fullname = '刘梅');
delete from trt_patient_case_history  where p_id in (select id from trt_patient  where fullname = '刘梅');
delete from trt_patient_doctor_info  where p_id in (select id from trt_patient  where fullname = '刘梅');