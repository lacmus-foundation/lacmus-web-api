using System.Text.Json.Serialization;

namespace Identity.ViewModels.Token
{
    public class TokenIssuer : IToken
    {
        [JsonPropertyName("access_token")]
        public AccessToken AccessToken { get; set; }
        [JsonPropertyName("exp")]
        public int Exp { get; set; }
    }
}