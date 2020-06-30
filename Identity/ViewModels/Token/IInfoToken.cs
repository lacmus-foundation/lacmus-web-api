namespace Identity.ViewModels.Token
{
    public interface IInfoToken
    {
        public string Aud { get; set; }
        public string Iss { get; set; }
        public string Sub { get; set; }
        public string Jti { get; set; }
    }
}