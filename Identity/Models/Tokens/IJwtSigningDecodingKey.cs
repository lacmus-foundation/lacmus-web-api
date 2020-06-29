using Microsoft.IdentityModel.Tokens;

namespace Identity.Models.Tokens
{
    public interface IJwtSigningDecodingKey
    {
        SecurityKey GetKey();
    }
}