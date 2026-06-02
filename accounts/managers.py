from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    
    def create_user(self, phone_number, email, full_name, password):# be tartib first username-field second required-field end password
        if not phone_number:
            raise ValueError("User must have phone number!!!")
        
        if not email:
            raise ValueError("User must have phone email!!!")

        if not full_name:
            raise ValueError("User must have full name!!")
        #django by default check password

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)#اگه اینجا پسورد رو بنویسم به صورت خام ذخیره میشه
        user.set_password(password)#hashing password
        user.save(using=self._db)
        return user
        
    def create_superuser(self, phone_number, email, full_name, password):
        #exactly like crate user one different is admin = true
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user