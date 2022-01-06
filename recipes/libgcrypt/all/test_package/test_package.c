#include "gcrypt.h"
#include "stdio.h"

int main() {
  printf("[TEST] gcrypt_md_open should work: ");
  gcry_md_hd_t handle;
  gcry_error_t result = gcry_md_open(&handle, 0, GCRY_MD_FLAG_HMAC);
  if (result) {
      printf("FAILURE\n");
      return result;
  }
  printf("SUCCESS\n");
  return 0;
}
