using Microsoft.IdentityModel.Tokens;

namespace Identity.Models.Tokens
{
    public interface IJwtEncryptingDecodingKey
    {
        SecurityKey GetKey();
    }
}