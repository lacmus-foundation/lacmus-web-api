using Microsoft.IdentityModel.Tokens;

namespace API_Identity.Models.Tokens
{
    public interface IJwtEncryptingDecodingKey
    {
        SecurityKey GetKey();
    }
}